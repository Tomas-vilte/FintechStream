from typing import Dict
from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.schema.binance_ticker_schema import binance_json_ticker_schema

TOPICS_CONFIG: Dict[str, dict] = {
    "binanceBookTicker": {
        "schema": binance_json_schema,
        "output_location": "/opt/bitnami/data_pipeline/raw_data/book_ticker",
        "checkpoint_location": "/opt/bitnami/data_pipeline/checkpoint/book_ticker"
    },
    "binanceTicker": {
        "schema": binance_json_ticker_schema,
        "output_location": "/opt/bitnami/data_pipeline/raw_data/ticker",
        "checkpoint_location": "/opt/bitnami/data_pipeline/checkpoint/ticker"
    },
}
