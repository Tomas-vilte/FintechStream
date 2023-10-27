package kafka

import (
	"context"
	"github.com/segmentio/kafka-go"
)

type KafkaProducer struct {
	Writer *kafka.Writer
}

func NewKafkaProducer(brokerAddress, topic string) (*KafkaProducer, error) {
	w := kafka.NewWriter(kafka.WriterConfig{
		Brokers: []string{brokerAddress},
		Topic:   topic,
	})

	return &KafkaProducer{Writer: w}, nil
}

func (kp *KafkaProducer) PublishData(data []byte) error {
	message := kafka.Message{
		Value: data,
	}

	return kp.Writer.WriteMessages(context.Background(), message)
}
