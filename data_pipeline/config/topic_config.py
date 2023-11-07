from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.schema.binance_ticker_schema import binance_json_ticker_schema

TOPICS_CONFIG: dict = {
    "binanceBookTicker": {
        "topic": "binanceBookTicker",
        "schema": binance_json_schema,
        "host": "broker:9092"
    },
    "binanceTrade": {
        "topic": "binanceTrade",
        "schema": binance_json_ticker_schema,
        "host": "broker:9092",
    }
}
