package utils

import (
	"encoding/json"
	"github.com/Tomas-vilte/FinanceStream/internal/config"
	"log"
)

func TransformData(data []byte, keyMapping config.KeyMapping) ([]byte, error) {
	var jsonData map[string]interface{}

	// Decodificar datos del json
	err := json.Unmarshal(data, &jsonData)
	if err != nil {
		log.Printf("Error a decodificar los datos: %s", err)
		return nil, err
	}

	// Aplicar transformacion de keys especificas del channel
	for oldKey, newKey := range keyMapping {
		if val, ok := jsonData[oldKey]; ok {
			jsonData[newKey] = val
			delete(jsonData, oldKey)
		}
	}

	// Codificar los datos del json
	transformedData, err := json.Marshal(jsonData)
	if err != nil {
		log.Printf("Hubo un error en codificar los datos: %s", err)
		return nil, err
	}

	return transformedData, nil
}
