package realtime

import (
	"github.com/gorilla/websocket"
	"log"
)

type BinanceWebSocket struct {
	Connection *websocket.Conn
}

func NewBinanceWebSocket(symbol, channel string) (*BinanceWebSocket, error) {
	url := "wss://stream.binance.us:9443/stream?streams=" + symbol + "@" + channel

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
			onDataReceived(msg)
		}
	}()
}
