package config

type ChannelConfig struct {
	Symbol     string
	Channel    string
	KafkaTopic string
}

type RealTimeConfig struct {
	BinanceChannels []ChannelConfig
	KafkaBroker     string
}
