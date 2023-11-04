from pyspark.sql.types import StructType
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json


def process_streaming(stream: DataFrame, stream_schema: StructType, topic: str):
    parsed_df = stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", stream_schema).alias("data")) \
        .select("data.*")

    return parsed_df
