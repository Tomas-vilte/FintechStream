package main

import (
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"github.com/Tomas-vilte/FinanceStream/internal/kafka"
	"github.com/Tomas-vilte/FinanceStream/internal/realtime"
	"log"
	"time"
)

func main() {

	kafkaConn, err := kafka.NewKafkaProducer("localhost:9092")
	if err != nil {
		log.Fatal("Error al crear la conexión a Kafka:", err)
		return
	}
	defer kafkaConn.Close()

	bookTickerConfig := config.ChannelConfig{
		Symbol:     "btcusdt",
		Channel:    "bookTicker",
		KafkaTopic: "binanceBookTicker",
	}

	bookTickerWS, err := realtime.NewBinanceWebSocket([]config.ChannelConfig{bookTickerConfig})
	if err != nil {
		log.Fatal("Error al crear la conexión WebSocket:", err)
		return
	}
	defer bookTickerWS.Close()
	go bookTickerWS.SubscribeToChannel(func(data []byte) {
		err := kafkaConn.PublishData("binanceBookTicker", data)
		if err != nil {
			log.Fatalf("Error al enviar datos a Kafka: %v\n", err)
		}
	})

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
	go tradeWS.SubscribeToChannel(func(data []byte) {
		err := kafkaConn.PublishData("binanceTrade", data)
		if err != nil {
			log.Fatalf("Error al enviar datos a Kafka: %v\n", err)
		}
	})

	time.Sleep(1 * time.Minute)

}
