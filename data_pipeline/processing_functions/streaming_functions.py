from pyspark.sql.streaming import DataStreamWriter
from pyspark.sql.types import StructType
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json


def process_streaming(stream: DataFrame, stream_schema: StructType) -> DataFrame:
    parsed_df = stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", stream_schema).alias("data")) \
        .select("data.*")

    return parsed_df


def create_file_write_stream(stream: DataFrame, storage_path: str, checkpoint_path: str,
                             file_format: str) -> DataStreamWriter:
    write_stream = stream.writeStream \
        .format(file_format) \
        .option("path", storage_path) \
        .option("checkpointLocation", checkpoint_path) \
        .trigger(processingTime="20 seconds") \
        .outputMode("append")

    return write_stream
