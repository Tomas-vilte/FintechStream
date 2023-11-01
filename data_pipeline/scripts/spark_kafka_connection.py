import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession, DataFrame
from typing import Optional


def create_spark_session(app: str) -> Optional[SparkSession]:
    try:
        conn = SparkSession.builder \
            .master("spark://172.28.0.2:7077") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3") \
            .appName(name=app) \
            .getOrCreate()

        conn.sparkContext.setLogLevel("ERROR")
        logging.info("Conexion creada con exito")
        return conn
    except Exception as error:
        logging.error(f"Hubo un error al crear la session de spark: {error}")
        return None


def connect_to_kafka(spark: SparkSession) -> Optional[DataFrame]:
    try:
        read_stream = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", TOPICS_CONFIG["broker"]) \
            .option("subscribe", TOPICS_CONFIG["binanceBookTicker"]["topic"]) \
            .load()

        logging.info(f"Conexion de kafka creada con exito")
        return read_stream
    except Exception as error:
        logging.error(f"Hubo un error al conectarse a kafka: {error}")
        return None


if __name__ == "__main__":
    spark_conn = create_spark_session("streamingBinance")

    if spark_conn is not None:
        read_stream_binance = connect_to_kafka(spark_conn)

        if read_stream_binance:
            query = read_stream_binance \
                .writeStream \
                .outputMode("append") \
                .format("console") \
                .start()
            try:
                query.awaitTermination(timeout=60)
            except KeyboardInterrupt as e:
                query.stop()
            except Exception as e:
                logging.error(f"Error en la ejecuccion: {e}")
        else:
            print("No se pudo conectar a kafka.")
    else:
        print("No se pudo crear la conexion de spark.")
