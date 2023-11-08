from pyspark.sql.types import StructField, StructType, StringType, IntegerType

binance_json_ticker_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("e", StringType(), True),
        StructField("E", IntegerType(), True),
        StructField("s", StringType(), True),
        StructField("p", StringType(), True),
        StructField("P", StringType(), True),
        StructField("w", StringType(), True),
        StructField("x", StringType(), True),
        StructField("c", StringType(), True),
        StructField("Q", StringType(), True),
        StructField("b", StringType(), True),
        StructField("B", StringType(), True),
        StructField("a", StringType(), True),
        StructField("A", StringType(), True),
        StructField("o", StringType(), True),
        StructField("h", StringType(), True),
        StructField("l", StringType(), True),
        StructField("v", StringType(), True),
        StructField("q", StringType(), True),
        StructField("O", IntegerType(), True),
        StructField("C", IntegerType(), True),
        StructField("F", IntegerType(), True),
        StructField("L", IntegerType(), True),
        StructField("n", IntegerType(), True)
    ]), True)
])
