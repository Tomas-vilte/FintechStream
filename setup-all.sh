#!/bin/bash

# Levantamos todos los contenedores.
docker compose up -d

# Creamos el usuario en superset
echo "Creando usuario en Superset"

# Le damos los permisos
chmod +x docker/docker-entrypoint-initdb.d/create-user.sh

# Ejecutamos el script para crear el usuario
bash docker/docker-entrypoint-initdb.d/create-user.sh

echo "IP del contenedor de Presto"
docker inspect \
  -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' presto