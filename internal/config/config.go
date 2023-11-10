package config

type KeyMapping map[string]string

type ChannelConfig struct {
	Symbol     string
	Channel    string
	KafkaTopic string
	KeyMapping KeyMapping
}

type RealTimeConfig struct {
	BinanceChannels []ChannelConfig
	KafkaBroker     string
}
