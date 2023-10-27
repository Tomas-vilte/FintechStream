package kafka

import "github.com/segmentio/kafka-go"

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
