from data_pipeline.config.topic_config import TOPICS_CONFIG
from pyspark.sql import SparkSession


def create_spark_session(app: str):
    return (
        SparkSession
        .builder
        .appName(name=app)
        .getOrCreate())


# spark = create_spark_session("test")
#
# read_stream = spark \
#                 .readStream \
#     .option(TOPICS_CONFIG[""])

print(TOPICS_CONFIG["binanceBookTicker"]["topic"])