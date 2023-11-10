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

	// Verificar si la clave data esta en el json
	if dataObj, ok := jsonData["data"].(map[string]interface{}); ok {

		// Aplicar la transformacion de la clave al objeto data
		for oldKey, newKey := range keyMapping {
			if val, ok := dataObj[oldKey]; ok {
				dataObj[newKey] = val
				delete(dataObj, oldKey)
			}
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
