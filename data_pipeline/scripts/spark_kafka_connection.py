import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession, DataFrame
from typing import Optional
from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.processing_functions.streaming_functions import process_streaming, create_file_write_stream


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
            .option("startingOffsets", "earliest") \
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
            parsed_df = process_streaming(
                read_stream_binance, binance_json_schema
            )

            query = (create_file_write_stream(
                parsed_df,
                "/opt/bitnami/data_pipeline/raw_data",
                "/opt/bitnami/data_pipeline/checkpoint",
                "json",
                "20 seconds"
            ).option("maxRecordsPerFile", 10000)
                     .start())

            console_query = parsed_df \
                .writeStream \
                .outputMode("append") \
                .format("console") \
                .start()

            try:
                console_query.awaitTermination(timeout=60)
                query.awaitTermination(timeout=60)
            except KeyboardInterrupt as e:
                console_query.stop()
                query.stop()
            except Exception as e:
                logging.error(f"Error en la ejecuccion: {e}")
        else:
            print("No se pudo conectar a kafka.")
    else:
        print("No se pudo crear la conexion de spark.")
