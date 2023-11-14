#!/bin/bash

# Espera a que el servicio de Superset esté listo
until docker exec -it superset superset db upgrade
do
  echo "Esperando que Superset esté listo..."
  sleep 2
done

# Comando para crear un usuario administrador
docker exec -it superset superset fab create-admin \
  --username "${ADMIN_USERNAME}" \
  --firstname "${ADMIN_FIRSTNAME}" \
  --lastname "${ADMIN_LASTNAME}" \
  --email "${ADMIN_EMAIL}" \
  --password "${ADMIN_PASSWORD}"

# Migrar la base de datos local de Superset a la última versión
docker exec -it superset superset db upgrade

# Configurar roles
docker exec -it superset superset init
