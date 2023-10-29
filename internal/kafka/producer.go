package kafka

import (
	"context"
	"fmt"
	"github.com/segmentio/kafka-go"
	"log"
)

type Producer struct {
	writer *kafka.Writer
}

func NewKafkaProducer(brokerAddress, topic string) (*Producer, error) {
	w := kafka.NewWriter(kafka.WriterConfig{
		Brokers: []string{brokerAddress},
		Topic:   topic,
	})
	fmt.Printf("Creado nuevo productor de Kafka para el tópico %s en el broker %s\n", topic, brokerAddress)
	return &Producer{writer: w}, nil
}

func (kp *Producer) PublishData(data []byte) error {
	message := kafka.Message{
		Value: data,
	}
	err := kp.writer.WriteMessages(context.Background(), message)
	if err != nil {
		log.Fatalf("Error al publicar en Kafka: %v\n", err)
	}
	return err
}

func (kp *Producer) Close() {
	kp.writer.Close()
}
