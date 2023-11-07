from pyspark.sql.types import StructField, StructType, StringType, LongType, DoubleType, IntegerType

binance_json_ticker_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("e", StringType(), True),
        StructField("E", LongType(), True),
        StructField("s", StringType(), True),
        StructField("p", DoubleType(), True),
        StructField("P", StringType(), True),
        StructField("w", DoubleType(), True),
        StructField("x", DoubleType(), True),
        StructField("c", DoubleType(), True),
        StructField("Q", DoubleType(), True),
        StructField("b", DoubleType(), True),
        StructField("B", DoubleType(), True),
        StructField("a", DoubleType(), True),
        StructField("A", DoubleType(), True),
        StructField("o", DoubleType(), True),
        StructField("h", DoubleType(), True),
        StructField("l", DoubleType(), True),
        StructField("v", DoubleType(), True),
        StructField("q", DoubleType(), True),
        StructField("O", LongType(), True),
        StructField("C", LongType(), True),
        StructField("F", IntegerType(), True),
        StructField("L", IntegerType(), True),
        StructField("n", IntegerType(), True),
    ]), True)
])
