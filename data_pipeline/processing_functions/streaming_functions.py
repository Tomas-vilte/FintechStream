import logging
from pyspark.sql.streaming import DataStreamWriter
from pyspark.sql.types import StructType
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json


def process_streaming(stream: DataFrame, stream_schema: StructType) -> DataFrame | None:
    """
       Procesa datos de streaming.

       Args:
           stream (DataFrame): El DataFrame de streaming de entrada.
           stream_schema (StructType): El esquema de los datos de streaming.

       Returns:
           DataFrame: El DataFrame procesado.
    """
    try:
        parsed_df = stream.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", stream_schema).alias("data")) \
            .select("data.*")
        logging.info("Procesamiento completado con exito")
        return parsed_df
    except Exception as error:
        logging.error(f"Error en el procesamiento de datos: {error}")
        return None


def create_file_write_stream(stream: DataFrame, storage_path: str, checkpoint_path: str,
                             file_format: str, trigger_interval: str) -> DataStreamWriter | None:
    """
       Configura la escritura en streaming.

       Args:
           stream (DataFrame): El DataFrame de streaming a escribir.
           storage_path (str): La ruta de almacenamiento.
           checkpoint_path (str): La ubicación de checkpoint.
           file_format (str): El formato de archivo.
           trigger_interval (str): El intervalo de disparo.

       Returns:
           DataStreamWriter: El objeto DataStreamWriter configurado.
    """
    try:
        write_stream = stream.writeStream \
            .format(file_format) \
            .option("path", storage_path) \
            .option("checkpointLocation", checkpoint_path) \
            .trigger(processingTime=trigger_interval) \
            .outputMode("append")

        logging.info("Guardado con exito")
        return write_stream
    except Exception as error:
        logging.error(f"Error en la configuracion de escritura en streaming: {error}")
        return None
