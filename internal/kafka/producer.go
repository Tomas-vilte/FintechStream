package kafka

import (
	"context"
	"github.com/segmentio/kafka-go"
)

type Producer struct {
	writer *kafka.Writer
}

func NewKafkaProducer(brokerAddress, topic string) (*Producer, error) {
	w := kafka.NewWriter(kafka.WriterConfig{
		Brokers: []string{brokerAddress},
		Topic:   topic,
	})
	return &Producer{writer: w}, nil
}

func (kp *Producer) PublishData(data []byte) error {
	message := kafka.Message{
		Value: data,
	}

	return kp.writer.WriteMessages(context.Background(), message)
}

func (kp *Producer) Close() {
	kp.writer.Close()
}
