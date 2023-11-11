from pyspark.sql.types import StructField, StructType, StringType, LongType

binance_json_ticker_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("eventType", StringType(), True),
        StructField("eventTime", LongType(), True),
        StructField("symbol", StringType(), True),
        StructField("priceChange", StringType(), True),
        StructField("priceChangePercent", StringType(), True),
        StructField("weightedAvgPrice", StringType(), True),
        StructField("firstTradePrice", StringType(), True),
        StructField("lastPrice", StringType(), True),
        StructField("lastQuantity", StringType(), True),
        StructField("bestBidPrice", StringType(), True),
        StructField("bestBidQuantity", StringType(), True),
        StructField("bestAskPrice", StringType(), True),
        StructField("bestAskQuantity", StringType(), True),
        StructField("openPrice", StringType(), True),
        StructField("highPrice", StringType(), True),
        StructField("lowPrice", StringType(), True),
        StructField("totalTradedBaseAssetVolume", StringType(), True),
        StructField("totalTradedQuoteAssetVolume", StringType(), True),
        StructField("statisticsOpenTime", LongType(), True),
        StructField("statisticsCloseTime", LongType(), True),
        StructField("firstTradeId", LongType(), True),
        StructField("lastTradeId", LongType(), True),
        StructField("totalNumberOfTrades", LongType(), True)

    ]))
])
