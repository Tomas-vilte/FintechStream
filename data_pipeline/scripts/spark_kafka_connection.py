import datetime
import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession, DataFrame


def create_spark_session(app: str) -> SparkSession | None:
    try:
        conn = SparkSession.builder \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
            .appName(name=app) \
            .getOrCreate()
        conn.sparkContext.setLogLevel("ERROR")
        logging.info("Conexion creada con exito")
        return conn
    except Exception as e:
        logging.error(f"Hubo un error al crear la session de spark: {e}")
        return None


def connect_to_kafka(spark: SparkSession) -> DataFrame | None:
    try:
        read_stream = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", TOPICS_CONFIG["broker"]) \
            .option("subscribe", TOPICS_CONFIG["binanceBookTicker"]["topic"]) \
            .option("includeHeaders", True) \
            .load()

        logging.info(f"Conexion de kafka creada con exito")
        return read_stream
    except Exception as e:
        logging.error(f"Hubo un error al conectarse a kafka: {e}")
        return None


if __name__ == "__main__":
    spark_conn = create_spark_session("streaming_binance")

    if spark_conn is not None:
        read_stream_binance = connect_to_kafka(spark_conn)

        if read_stream_binance:
            query = read_stream_binance \
                .writeStream \
                .outputMode("append") \
                .format("console") \
                .start()

            query.awaitTermination(timeout=)
        else:
            print("No se pudo conectar a kafka.")
    else:
        print("No se pudo crear la conexion de spark.")