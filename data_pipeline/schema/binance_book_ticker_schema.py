from pyspark.sql.types import StructType, StructField, StringType, IntegerType

binance_json_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("updateId", IntegerType(), True),
        StructField("symbol", StringType(), True),
        StructField("bestBidPrice", StringType(), True),
        StructField("bestBidQuantity", StringType(), True),
        StructField("bestAskPrice", StringType(), True),
        StructField("bestAskQuantity", StringType(), True),
    ]), True)
])
