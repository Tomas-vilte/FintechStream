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

## Ejecuccion del Recolector de Datos
1. Despues de la configuracion, movete al directorio `cmd`, donde se encuentra el archivo `main.go`, que comienza a recolectar los datos y enviarlos al topic.
```bash
cd cmd
go run main.go
```

## Enviar Job al cluster de Spark
1. Primero accede a http://localhost:8080 en tu navegador.
2. Copia la IP de Spark Master que se muestra en la interfaz web, es la que dice `URL`.
3. Luego, entra al contenedor `fintechstream-spark-master-1` y cambia al directorio principal:
```bash
docker exec -it fintechstream-spark-master-1 bash
cd ..
```
4. Ejecuta el siguiente comando para enviar el job al cluster de Spark, reemplazando `IP_de_Spark_Master` con la IP que copiaste anteriormente:
```bash
spark-submit --master spark://IP_de_Spark_Master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 data_pipeline/scripts/spark_kafka_connection.py
```

## Resultado del job de Spark
![resultado](/images/job_result.png)

## Tabla en ScyllaDB
![tabla](/images/table_scylladb.png)

## Análisis Realizado

### Análisis 1: Datos de Libro de Órdenes (Binance Book Ticker Data)
- **Descripción:** Este análisis examina la evolución de las máximas ofertas de compra (best_bid_price) y de venta (best_ask_price) para diferentes símbolos, como BTCUSDT y ETHUSDT, a lo largo del tiempo, según los datos del libro de órdenes de Binance.

- **Visualización:** El gráfico "Evolución de Máximas Ofertas de Compra y Venta por Símbolo" ilustra cómo han variado las ofertas de compra y venta para los símbolos seleccionados en cada actualización de datos.

    ![grafico1](/images/Evolución%20de%20Máximas%20Ofertas%20de%20Compra%20y%20Venta%20por%20Símbolo.png)

### Análisis 2: Datos de Ticker (Binance Ticker Data)
- **Descripción:** El análisis de los "Datos de Transacciones" (Binance Ticker Data) se centra en el número total de operaciones (total_number_of_trades) para los pares de criptomonedas BTCUSDT y ETHUSDT a lo largo del tiempo.

- **Visualización:** Este gráfico de barras representa el número total de operaciones (total_number_of_trades) para los pares de criptomonedas BTCUSDT y ETHUSDT a lo largo del tiempo, según los datos de transacciones de Binance.

    ![graficos2](/images/número%20total%20de%20operaciones.png)