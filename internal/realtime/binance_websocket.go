package realtime

import (
	"fmt"
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"github.com/Tomas-vilte/FinanceStream/internal/kafka"
	"github.com/gorilla/websocket"
	"log"
)

type BinanceWebSocket struct {
	Connection *websocket.Conn
}

func SubscribeAndPublish(ws *BinanceWebSocket, kafkaConn *kafka.Producer, kafkaTopic string) {
	go ws.SubscribeToChannel(func(data []byte) {
		fmt.Printf("Recibiendo data de Binance: %v\n", string(data))
		err := kafkaConn.PublishData(kafkaTopic, data)
		if err != nil {
			log.Fatalf("Error al enviar datos a Kafka para %s: %v\n", kafkaTopic, err)
		}
	})
}

func NewBinanceWebSocket(channels []config.ChannelConfig) (*BinanceWebSocket, error) {
	url := "wss://stream.binance.us:9443/stream?streams="
	for i, channel := range channels {
		if i > 0 {
			url += "/"
		}
		url += channel.Symbol + "@" + channel.Channel
	}

	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Printf("Hubo un error al conectarse: %v", err)
		return nil, err
	}

	return &BinanceWebSocket{Connection: conn}, nil
}
func (ws *BinanceWebSocket) SubscribeToChannel(onDataReceived func([]byte)) {
	go func() {
		for {
			_, msg, err := ws.Connection.ReadMessage()
			if err != nil {
				log.Printf("Error al leer mensaje: %v", err)
				return
			}

			// Llamar a la función onDataReceived con el mensaje y el canal
			onDataReceived(msg)
		}
	}()
}

func (ws *BinanceWebSocket) Close() {
	ws.Connection.Close()
}
