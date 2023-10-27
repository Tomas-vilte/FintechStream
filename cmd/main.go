package main

import (
	"fmt"
	"github.com/Tomas-vilte/FinanceStream/internal/kafka"
	"github.com/Tomas-vilte/FinanceStream/internal/realtime"
	"log"
	"time"
)

func main() {

	// Configuración de Binance WebSocket
	symbol := "btcusdt"
	channel := "bookTicker"

	binanceWS, err := realtime.NewBinanceWebSocket(symbol, channel)
	if err != nil {
		log.Fatal("Error al crear la conexión WebSocket:", err)
		return
	}
	defer binanceWS.Close()

	// Configuración de Kafka
	brokerAddress := "localhost:9092"
	kafkaTopic := "bookTicker"

	kafkaProducer, err := kafka.NewKafkaProducer(brokerAddress, kafkaTopic)
	if err != nil {
		fmt.Printf("Error al crear el productor Kafka: %v\n", err)
		return
	}
	defer kafkaProducer.Close()

	// Función para manejar los datos recibidos desde Binance y publicar en Kafka
	onDataReceived := func(data []byte) {
		fmt.Printf("Datos recibidos de Binance: %s\n", string(data))

		// Publica los datos en Kafka
		if err := kafkaProducer.PublishData(data); err != nil {
			fmt.Printf("Error al publicar en Kafka: %v\n", err)
		}
	}

	// Suscripción a Binance WebSocket y procesamiento de datos
	binanceWS.SubscribeToChannel(onDataReceived)

	time.Sleep(10 * time.Minute)
}
