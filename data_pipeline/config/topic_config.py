from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.schema.binance_ticker_schema import binance_json_ticker_schema

TOPICS_CONFIG: dict = {
    "host": "broker:9092",
    "binanceBookTicker": {
        "topic": "binanceBookTicker",
        "schema": binance_json_schema
    },
    "binanceTrade": {
        "topic": "binanceTrade",
        "schema": binance_json_ticker_schema
    }
}
