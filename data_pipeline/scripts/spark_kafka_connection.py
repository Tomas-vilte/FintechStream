import logging
from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession


def create_spark_session(app: str):
    try:
        conn = SparkSession.builder \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
            .appName(name=app) \
            .getOrCreate()
        conn.sparkContext.setLogLevel("ERROR")
        logging.info("Conexion creada con exito")
    except Exception as e:
        logging.error(f"Hubo un error al crear la session de spark: {e}")




