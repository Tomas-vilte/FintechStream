import logging
from pyspark.sql import SparkSession, DataFrame
from typing import Optional
from data_pipeline.config.topic_config import TOPICS_CONFIG
from data_pipeline.processing_functions.streaming_functions import process_streaming, create_file_write_stream
from pyspark.errors import AnalysisException, StreamingQueryException


def create_spark_session(app: str) -> Optional[SparkSession]:
    """
        Crea una sesión de Spark.

        Args:
            app (str): El nombre de la aplicación Spark.

        Returns:
            SparkSession: La sesión de Spark creada o None si hay un error.
        """
    try:
        conn = SparkSession.builder \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3") \
            .appName(name=app) \
            .getOrCreate()

        conn.sparkContext.setLogLevel("ERROR")
        logging.info("Conexion creada con exito")
        return conn
    except AnalysisException as ERROR:
        logging.error(f"Error de analisis: {ERROR}")
    except Exception as ERROR:
        logging.error(f"Hubo un error al crear la session de spark: {ERROR}")
    return None


def connect_to_kafka(spark: SparkSession, topics: str) -> Optional[DataFrame]:
    """
        Conecta a un servidor Kafka y recupera datos de streaming.

        Args:
            spark (SparkSession): La sesión de Spark.
            topics (str): Los temas de Kafka a los que suscribirse.

        Returns:
            DataFrame: El DataFrame de streaming creado o None si hay un error.
        """
    try:
        read_streams = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "broker:9092") \
            .option("startingOffsets", "earliest") \
            .option("failOnDataLoss", "false") \
            .option("subscribe", topics) \
            .load()

        logging.info(f"Conexión de Kafka creada con éxito")
        return read_streams
    except StreamingQueryException as e:
        logging.error(f"Error de consulta de streaming: {e}")
    except AnalysisException as e:
        logging.error(f"Error de análisis: {e}")
    except Exception as e:
        logging.error(f"Hubo un error al conectarse a kafka: {e}")
    return None


if __name__ == "__main__":
    spark_conn = create_spark_session("streamingBinance")

    if spark_conn is not None:
        query_streams = {}

        for topic, config in TOPICS_CONFIG.items():
            read_stream = connect_to_kafka(spark_conn, topic)
            parsed_df = process_streaming(read_stream, config["schema"])
            query_stream = create_file_write_stream(
                parsed_df,
                config["output_location"],
                config["checkpoint_location"],
                "10 seconds",
                "json"
            )
            query_streams[topic] = query_stream

            try:
                for query in query_streams.values():
                    query.awaitTermination(timeout=30)
            except KeyboardInterrupt as error:
                for query in query_streams.values():
                    query.stop()
            except Exception as error:
                logging.error(f"Error en la ejecuccion: {error}")
        else:
            logging.error("No se pudo crear la conexión de Spark")