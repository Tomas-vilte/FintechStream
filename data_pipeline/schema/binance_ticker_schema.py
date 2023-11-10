from pyspark.sql.types import StructField, StructType, StringType, LongType

binance_json_ticker_schema = StructType([
    StructField("stream", StringType(), True),
    StructField("data", StructType([
        StructField("eventType", StringType(), True),
        StructField("eventTime", LongType(), True),
        StructField("symbol", StringType(), True),
        StructField("priceChange", StringType(), True),
        StructField("priceChangePercent", StringType(), True),
        StructField("weightedAveragePrice", StringType(), True),
        StructField("firstTrade", StringType(), True),
        StructField("lastPrice", StringType(), True),
        StructField("lastQuantity", StringType(), True),
        StructField("bestBidPrice", StringType(), True),
        StructField("bestBidQuantity", StringType(), True),
        StructField("bestAskPrice", StringType(), True),
        StructField("bestAskQuantity", StringType(), True),
        StructField("openPrice", StringType(), True),
        StructField("highPrice", StringType(), True),
        StructField("lowPrice", StringType(), True),
        StructField("totalTraded", StringType(), True),
        StructField("totalTradedQuote", StringType(), True),
        StructField("statisticOpenTime", LongType(), True),
        StructField("statisticCloseTime", LongType(), True),
        StructField("firstTradeId", LongType(), True),
        StructField("lastTradeId", LongType(), True),
        StructField("totalTrades", LongType(), True)

    ]))
])
