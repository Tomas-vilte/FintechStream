import logging
from typing import Optional
from pyspark.errors import AnalysisException, StreamingQueryException
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json, col, to_json


def process_and_write_to_location(output_location: str, file_format: str, json_schema):
    def foreach_batch_function(df: DataFrame, batch_id: int):
        try:
            df = df.select("data.*")

            df.printSchema()
            df.show()
            df.write.format(file_format).mode("append").save(output_location)
            logging.info("Escritura completada con exito")
        except Exception as error:
            logging.error(f"Error en la escritura de datos: {error}")

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
    except AnalysisException as error:
        logging.error(f"Error de análisis: {error}")
    except Exception as error:
        logging.error(f"Error en el procesamiento de datos: {error}")
        return None


def create_file_write_stream(stream: DataFrame, storage_path: str, checkpoint_path: str,
                             trigger_interval: str, schema: StructType, file_format: str = "parquet") -> Optional[StreamingQuery]:
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
        write_stream = stream.coalesce(1).writeStream \
            .option("checkpointLocation", checkpoint_path) \
            .trigger(processingTime=trigger_interval) \
            .outputMode("append") \
            .foreachBatch(process_and_write_to_location(storage_path, file_format, schema)) \
            .start()

        logging.info("Guardado con exito")
        return write_stream
    except AnalysisException as error:
        logging.error(f"Error de análisis: {error}")
    except StreamingQueryException as error:
        logging.error(f"Error en la consulta de streaming: {error}")
    except Exception as error:
        logging.error(f"Error en la configuración de escritura en streaming: {error}")
        return None
