package main

import (
	"github.com/Tomas-vilte/FinanceStream/app"
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"log"
)

func main() {
	appConfig := config.RealTimeConfig{
		BinanceChannels: []config.ChannelConfig{
			{
				Symbol:     "btcusdt",
				Channel:    "bookTicker",
				KafkaTopic: "binanceBookTicker",
			},
			{
				Symbol:     "btcusdt",
				Channel:    "ticker",
				KafkaTopic: "binanceTrade",
			},
		},
		KafkaBroker: "localhost:9092",
	}

	err := app.RunApplication(appConfig)
	if err != nil {
		log.Fatalf("Error en la aplicacion: %v", err)
	}
}
