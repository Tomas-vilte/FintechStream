package main

import (
	"fmt"
	"github.com/Tomas-vilte/FinanceStream/internal/realtime"
	"log"
)

func onDataReceived(data []byte) {
	fmt.Printf("Data recibida: %s\n", string(data))
}

func main() {
	symbol := "btcusdt"
	channels := []string{
		symbol + "@bookTicker",
		symbol + "@trade",
		symbol + "@ticker",
		symbol + "@aggTrade",
	}

	err := realtime.SubscribeToBinanceStreams(channels, onDataReceived)
	if err != nil {
		log.Fatal("Error al suscribirse a los canales de Binance:", err)
	}
}
