package realtime

import (
	"github.com/gorilla/websocket"
	"log"
	"strings"
)

func SubscribeToBinanceStreams(channels []string, onDataReceived func([]byte)) error {
	// URL del servidor WebSocket de Binance
	url := "wss://stream.binance.us:9443/stream?streams=" + strings.Join(channels, "/")

	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Printf("Hubo un error al conectarse: %v\n", err)
		return err
	}
	defer conn.Close()

	// Mensaje de suscripción a los canales
	subscriptionMessage := map[string]interface{}{
		"method": "SUBSCRIBE",
		"params": channels,
		"id":     1,
	}

	// Envía el mensaje de suscripción al servidor
	if err := conn.WriteJSON(subscriptionMessage); err != nil {
		log.Printf("Hubo un error al escribir el mensaje: %v", err)
		return err
	}

	// Goroutine para recibir datos en tiempo real
	go func() {
		for {
			_, msg, err := conn.ReadMessage()
			if err != nil {
				log.Printf("Error al leer mensaje: %v", err)
				return
			}

			onDataReceived(msg)
		}
	}()

	select {}
}
