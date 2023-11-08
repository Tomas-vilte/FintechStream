import logging
from typing import Optional
from pyspark.sql.streaming import DataStreamWriter, StreamingQuery
from pyspark.sql.types import StructType
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json


def process_and_write_to_location(output_location: str):
    def foreach_batch_function(df, batch_id):
        df.write.format("json").mode("append").save(output_location)

    return foreach_batch_function


def process_streaming(stream: DataFrame, stream_schema: StructType) -> Optional[DataFrame]:
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
                             trigger_interval: str, file_format: str = "parquet", ) -> Optional[StreamingQuery]:
    """
       Configura la escritura en streaming.

       Args:
           stream (DataFrame): El DataFrame de streaming a escribir.
           storage_path (str): La ruta de almacenamiento.
           checkpoint_path (str): La ubicación de checkpoint.
           file_format (str): El formato de archivo por default es parquet, sino se especifica.
           trigger_interval (str): El intervalo de disparo.

       Returns:
           StreamingQuery: El objeto StreamingQuery configurado.
    """
    try:
        write_stream = stream.writeStream \
            .format(file_format) \
            .option("checkpointLocation", checkpoint_path) \
            .trigger(processingTime=trigger_interval) \
            .outputMode("append") \
            .foreachBatch(process_and_write_to_location(storage_path)) \
            .start()

        logging.info("Guardado con exito")
        return write_stream
    except Exception as error:
        logging.error(f"Error en la configuracion de escritura en streaming: {error}")
        return None
