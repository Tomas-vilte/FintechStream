package app

import (
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"github.com/Tomas-vilte/FinanceStream/internal/kafka"
	"github.com/Tomas-vilte/FinanceStream/internal/realtime"
	"log"
	"time"
)

func RunApplication(appConfig config.RealTimeConfig) error {
	// Conexion con kafka
	kafkaConn, err := kafka.NewKafkaProducer(appConfig.KafkaBroker)
	if err != nil {
		log.Fatal("Error al crear la conexión a Kafka:", err)
		return err
	}
	defer kafkaConn.Close()

	for _, channelConfig := range appConfig.BinanceChannels {
		channelWS, err := realtime.NewBinanceWebSocket([]config.ChannelConfig{channelConfig})
		if err != nil {
			log.Fatalf("Error al crear la conexión WebSocket para %s: %v\n", channelConfig.Channel, err)
			return err
		}
		defer channelWS.Close()

		// Suscribirse y Publicar en kafka
		realtime.SubscribeAndPublish(channelWS, kafkaConn, channelConfig.KafkaTopic)
	}
	time.Sleep(1 * time.Minute)

	return nil
}
