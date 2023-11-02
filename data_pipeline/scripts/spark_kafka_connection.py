import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession, DataFrame
from typing import Optional
from pyspark.sql.functions import from_json
from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema


def create_spark_session(app: str) -> Optional[SparkSession]:
    try:
        conn = SparkSession.builder \
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
            .option("kafka.bootstrap.servers", TOPICS_CONFIG["host"]) \
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
            parsed_df = read_stream_binance.selectExpr("CAST(value AS STRING) as json") \
                .select(from_json("json", binance_json_schema).alias("data")) \
                .select("data.*")

            json_df = parsed_df.selectExpr("to_json(struct(*)) AS jsonData")

            query = json_df \
                .writeStream \
                .foreachBatch() \
                .outputMode("append") \
                .start()

            console_query = parsed_df \
                .writeStream \
                .outputMode("append") \
                .format("console") \
                .start()

            try:
                query.awaitTermination(timeout=60)
                console_query.awaitTermination(timeout=60)
            except KeyboardInterrupt as e:
                query.stop()
                console_query.stop()
            except Exception as e:
                logging.error(f"Error en la ejecuccion: {e}")
        else:
            print("No se pudo conectar a kafka.")
    else:
        print("No se pudo crear la conexion de spark.")
