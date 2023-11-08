import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession, DataFrame
from typing import Optional
from data_pipeline.processing_functions.streaming_functions import process_streaming, create_file_write_stream
from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.schema.binance_ticker_schema import binance_json_ticker_schema


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


def connect_to_kafka(spark: SparkSession, topic: str) -> Optional[DataFrame]:
    try:
        read_stream = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "broker:9092") \
            .option("startingOffsets", "earliest") \
            .option("failOnDataLoss", "false") \
            .option("subscribe", TOPICS_CONFIG[topic]["topic"]) \
            .load()

        logging.info(f"Conexión de Kafka creada con éxito")
        return read_stream
    except Exception as error:
        logging.error(f"Hubo un error al conectarse a kafka: {error}")
        return None


if __name__ == "__main__":
    spark_conn = create_spark_session("streamingBinance")

    if spark_conn is not None:
        read_stream_bookTicker = connect_to_kafka(spark_conn, "binanceBookTicker")
        read_stream_Ticker = connect_to_kafka(spark_conn, "binanceTicker")

        parsed_df_bookTicker = process_streaming(
            read_stream_bookTicker, binance_json_schema
        )

        parsed_df_Ticker = process_streaming(
            read_stream_Ticker, binance_json_ticker_schema
        )

        query_bookTicker = create_file_write_stream(
            parsed_df_bookTicker,
            "/opt/bitnami/data_pipeline/raw_data/book_ticker",
            "/opt/bitnami/data_pipeline/checkpoint",
            "5 seconds",
            "json"
        )

        query_Ticker = create_file_write_stream(
            parsed_df_Ticker,
            "/opt/bitnami/data_pipeline/raw_data/ticker",
            "/opt/bitnami/data_pipeline/checkpoint",
            "5 seconds",
            "json"
        )

        query_bookTicker.awaitTermination(timeout=30)
        query_Ticker.awaitTermination(timeout=30)
