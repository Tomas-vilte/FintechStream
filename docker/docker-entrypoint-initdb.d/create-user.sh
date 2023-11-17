#!/bin/bash

# Espera a que el servicio de Superset esté listo
until docker exec -it superset superset db upgrade
do
  echo "Esperando que Superset esté listo..."
  sleep 2
done

# Comando para crear un usuario administrador utilizando variables de entorno
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin

# Migrar la base de datos local de Superset a la última versión
docker exec -it superset superset db upgrade

# Configurar roles
docker exec -it superset superset init