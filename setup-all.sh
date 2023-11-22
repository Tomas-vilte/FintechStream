#!/bin/bash

# Levantamos todos los contenedores.
docker compose up -d

# Creamos el usuario en superset
echo "Creando usuario en Superset"

# Le damos los permisos
chmod +x docker/docker-entrypoint-initdb.d/create-user.sh

# Ejecutamos el script para crear el usuario
bash docker/docker-entrypoint-initdb.d/create-user.sh

# Creamos los topics de Kafka
echo "Creando los topics de Kafka"
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic binanceTicker
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic binanceBookTicker

presto_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' presto)
echo "Los contenedores se han levantado exitosamente."
echo "La IP de Presto es: $presto_ip"