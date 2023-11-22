#!/bin/bash


# Ruta del archivo .cql
CQL_FILE="docker-entrypoint-initdb.d/schema.cql"

# Comando para ejecutar el script CQL
docker exec -it scylladb cqlsh -f $CQL_FILE 
