from typing import Dict
from data_pipeline.schema.binance_book_ticker_schema import binance_json_schema
from data_pipeline.schema.binance_ticker_schema import binance_json_ticker_schema

TOPICS_CONFIG: Dict[str, dict] = {
    "binanceBookTicker": {
        "schema": binance_json_schema,
        "output_location": "/opt/bitnami/data_pipeline/raw_data/book_ticker",
        "checkpoint_location": "/opt/bitnami/data_pipeline/checkpoint/book_ticker",
        "host_scyllaDB": "172.19.0.6",
        "port_scyllaDB": "9042",
        "table": "binance_book_ticker_data"
    },
    "binanceTicker": {
        "schema": binance_json_ticker_schema,
        "output_location": "/opt/bitnami/data_pipeline/raw_data/ticker",
        "checkpoint_location": "/opt/bitnami/data_pipeline/checkpoint/ticker",
        "host_scyllaDB": "172.19.0.6",
        "port_scyllaDB": "9042",
        "table": "binance_ticker_data",
    },
}
