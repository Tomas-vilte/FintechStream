package main

import (
	"log"

	"github.com/Tomas-vilte/FinanceStream/app"
	"github.com/Tomas-vilte/FinanceStream/internal/config"
)

func main() {
	appConfig := config.RealTimeConfig{
		BinanceChannels: []config.ChannelConfig{
			{
				Symbol:     "btcusdt",
				Channel:    "bookTicker",
				KafkaTopic: "binanceBookTicker",
				KeyMapping: config.KeyMapping{
					"u": "updateId",
					"s": "symbol",
					"b": "bestBidPrice",
					"B": "bestBidQuantity",
					"a": "bestAskPrice",
					"A": "bestAskQuantity",
				},
			},
			{
				Symbol:     "btcusdt",
				Channel:    "ticker",
				KafkaTopic: "binanceTicker",
			},
		},
		KafkaBroker: "localhost:9092",
	}

	err := app.RunApplication(appConfig)
	if err != nil {
		log.Fatalf("Error en la aplicacion: %v", err)
	}
}
