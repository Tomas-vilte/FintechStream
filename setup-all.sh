#!/bin/bash

# Levantamos todos los contenedores.
docker compose up -d

# # Creamos el usuario en superset
# echo "Creando usuario en Superset"

# # Le damos los permisos
# chmod +x docker/docker-entrypoint-initdb.d/create-user.sh

# # Ejecutamos el script para crear el usuario
# bash docker/docker-entrypoint-initdb.d/create-user.sh

# Creamos las tablas de cassandra
#docker exec -it scylladb docker-entrypoint-initdb.d/setup-cassandra.sh
bash docker/docker-entrypoint-initdb.d/setup-cassandra.sh