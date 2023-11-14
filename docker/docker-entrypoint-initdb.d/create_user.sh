#!/bin/bash

# Espera a que el servicio de Superset esté listo
until docker exec -it superset_container_name superset db upgrade
do
  echo "Esperando que Superset esté listo..."
  sleep 2
done

# Comando para crear un usuario administrador utilizando variables de entorno
docker exec -it superset superset fab create-admin \
  --username "$ADMIN_USERNAME" \
  --firstname "$ADMIN_FIRSTNAME" \
  --lastname "$ADMIN_LASTNAME" \
  --email "$ADMIN_EMAIL" \
  --password "$ADMIN_PASSWORD"
