package realtime

import (
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"github.com/gorilla/websocket"
	"log"
)

type BinanceWebSocket struct {
	Connection *websocket.Conn
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
