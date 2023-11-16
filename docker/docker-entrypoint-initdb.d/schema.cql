-- Parte 1: Crear Keyspace
CREATE KEYSPACE IF NOT EXISTS binance_stream WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 1};

-- Parte 2: Crear Tablas
USE binance_stream;

CREATE TABLE IF NOT EXISTS binance_book_ticker_data (
   id UUID PRIMARY KEY,
   stream text,
   update_id int,
   symbol text,
   best_bid_price text,
   best_bid_quantity text,
   best_ask_price text,
   best_ask_quantity text
);

CREATE TABLE IF NOT EXISTS binance_ticker_data (
   id UUID PRIMARY KEY,
   stream text,
   event_type text,
   event_time bigint,
   symbol text,
   price_change text,
   price_change_percent text,
   weighted_avg_price text,
   first_trade_price text,
   last_price text,
   last_quantity text,
   best_bid_price text,
   best_bid_quantity text,
   best_ask_price text,
   best_ask_quantity text,
   open_price text,
   high_price text,
   low_price text,
   total_traded_base_asset_volume text,
   total_traded_quote_asset_volume text,
   statistics_open_time bigint,
   statistics_close_time bigint,
   first_trade_id bigint,
   last_trade_id bigint,
   total_number_of_trades bigint
);
