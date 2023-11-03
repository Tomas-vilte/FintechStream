from pyspark.sql.types import StructType, StructField, StringType, IntegerType

binance_json_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("u", IntegerType(), True),
        StructField("s", StringType(), True),
        StructField("b", StringType(), True),
        StructField("B", StringType(), True),
        StructField("a", StringType(), True),
        StructField("A", StringType(), True),
    ]), True)
])