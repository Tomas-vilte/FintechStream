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
                             file_format: str) -> DataStreamWriter:
    write_stream = stream.writeStream \
        .format(file_format) \
        .option("path", storage_path) \
        .option("checkpointLocation", checkpoint_path) \
        .trigger(processingTime="20 seconds") \
        .outputMode("append")

    return write_stream
