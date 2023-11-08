from pyspark.sql.types import StructField, StructType, StringType, LongType

binance_json_ticker_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("e", StringType(), True),
        StructField("E", LongType(), True),
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
        StructField("O", LongType(), True),
        StructField("C", LongType(), True),
        StructField("F", LongType(), True),
        StructField("L", LongType(), True),
        StructField("n", LongType(), True)

    ]))
])
