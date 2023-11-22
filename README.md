# FintechStream

## Descripcion

Este proyecto tiene como objetivo recolectar, procesar y analizar datos financieros en tiempo real utilizando la API de Binance a través de WebSockets. La arquitectura del proyecto se basa en la recolección de datos en Golang, transmisión a través de Apache Kafka, procesamiento en tiempo real con Apache Spark Streaming, almacenamiento en ScyllaDB, y visualización mediante Apache Superset. Todos los servicios se gestionan y ejecutan en contenedores Docker para facilitar la implementación y escalabilidad.

# Componentes Principales

1. Recolector de Datos (Golang)
Utilice Go para consumir datos de la API de Binance a traves de WebSockets. Este componente es responsable de la recoleccion de datos en tiempo real desde diferentes topics.

2. Transmision de datos (Apache Kafka)
Apache Kafka actua como plataforma de transmision de datos, donde cada topic corresponde a un channel especifico de WebSocket. Los datos recolectados se envian a sus respectivos topics en kafka, permitiendo una separacion y gestion eficientes de los flujos de datos.

3. Procesamiento en tiempo real (Apache Spark Streaming)
Spark se encarga de consumir datos desde los topics de Kafka y realizar analisis en tiempo real. Pueden aplicarse transformaciones, agregaciones y logica de procesamiento segun los requerimientos de cada topic.

4. Almacenamiento de Datos (ScyllaDB)
ScyllaDB se utiliza como base de datos NoSQL para almacenar los datos procesados y permitir consultas eficientes en tiempo real.

5. Visualizacion de Datos (Apache Superset)
Utilice Apache Superset para visualizar los datos almacenados en ScyllaDB, proporcionando paneles interactivos y dashboards para el analisis y la toma de decisiones.

6. Orquestacion de Contenedores (Docker)
Todos los servicios se gestionan y ejecutan en contenedores Docker, lo que simplifica la implementacion, la gestion de dependencias y la escalabilidad de la infraestructura.

## Configuracion y Ejecuccion

Ejecuta el siguiente script para levantar todos los servicios en contenedores Docker:
```bash
setup-all.sh
```
Este script también proporcionará la IP de Presto para su configuración en Superset.

## Configuracion de ScyllaDB
Despues de levantar los contenedores, ingresa al contenedor de ScyllaDB y ejecuta el script `setup-cassandra.sh`:
```bash
docker exec -it scylladb bash #Una vez dentro del contenedor
cd docker-entrypoint-initdb.d/
bash setup-cassandra.sh #Este script creara las tablas
```

## Configuracion de Superset
1. Una vez que se ejecuta los contenedores y esta todo ok. Accede a http://localhost:8088/superset/welcome/
2. Coloca las credenciales. En este caso el usuario es admin, y la contraseña es admin.
3. Dirigite a "Data" -> "Databases Connections" en el menu de Superset
4. Haz click en el boton "Create" para agregar una nueva base de datos
5. Completa los detalles, y en la seccion "SQLALCHEMY URI", ingresa la URL de conexion a Presto:
```
presto://172.19.0.3:8085/scylladb
```
!Acordate de poner la IP que se imprime cuando se ejecuta el script `setup-all.sh`

