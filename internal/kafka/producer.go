package kafka

import (
	"context"
	"github.com/segmentio/kafka-go"
	"log"
	"time"
)

type Producer struct {
	writer *kafka.Writer
}

func NewKafkaProducer(brokerAddress string) (*Producer, error) {
	config := kafka.WriterConfig{
		Brokers:      []string{brokerAddress},
		Topic:        "",
		Balancer:     &kafka.LeastBytes{},
		BatchSize:    1000,
		BatchBytes:   1048576,
		BatchTimeout: 100 * time.Microsecond,
	}
	writer := kafka.NewWriter(config)

	return &Producer{writer: writer}, nil
}

func (kp *Producer) PublishData(topic string, data []byte) error {
	message := kafka.Message{
		Topic: topic,
		Key:   nil,
		Value: data,
	}
	err := kp.writer.WriteMessages(context.Background(), message)
	if err != nil {
		log.Fatalf("Error al publicar en Kafka: %v\n", err)
		return err
	}
	return nil
}

func (kp *Producer) Close() {
	kp.writer.Close()
}
