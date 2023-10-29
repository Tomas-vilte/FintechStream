package main

import (
	"fmt"
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"github.com/Tomas-vilte/FinanceStream/internal/realtime"
	"log"
	"time"
)

func main() {

	onDataReceived := func(data []byte) {
		fmt.Printf("Datos recibidos de Binance: %s\n", string(data))
	}

	bookTickerConfig := config.ChannelConfig{
		Symbol:     "btcusdt",
		Channel:    "bookTicker",
		KafkaTopic: "bookTicker",
	}

	binanceWS, err := realtime.NewBinanceWebSocket([]config.ChannelConfig{bookTickerConfig})
	if err != nil {
		log.Fatal("Error al crear la conexión WebSocket:", err)
		return
	}
	defer binanceWS.Close()
	go binanceWS.SubscribeToChannel(onDataReceived)

	tradeConfig := config.ChannelConfig{
		Symbol:     "btcusdt",
		Channel:    "ticker",
		KafkaTopic: "binanceTrade",
	}

	tradeWS, err := realtime.NewBinanceWebSocket([]config.ChannelConfig{tradeConfig})
	if err != nil {
		log.Printf("Error al crear la conexión WebSocket para trade: %v\n", err)
		return
	}
	defer tradeWS.Close()
	go tradeWS.SubscribeToChannel(onDataReceived)

	time.Sleep(1 * time.Minute)

}
