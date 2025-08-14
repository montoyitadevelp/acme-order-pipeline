# 🛒 E-commerce Orders Service

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red?logo=python)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.x-green?logo=mongodb)](https://www.mongodb.com/)
[![Kafka](https://img.shields.io/badge/Apache-Kafka-black?logo=apache-kafka)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)
[![SwaggerUI](https://img.shields.io/badge/Swagger-UI-orange?logo=swagger)](https://swagger.io/tools/swagger-ui/)


## 📌 Finalidad de la prueba técnica
Este proyecto corresponde a una **prueba técnica** cuyo objetivo es demostrar la capacidad de diseñar y construir un servicio backend orientado a la gestión de un **sistema de e-commerce**.  
El servicio maneja **órdenes, productos e inventario** utilizando principios de arquitectura limpia, separación de responsabilidades y comunicación asincrónica con Kafka para manejar eventos distribuidos.  


---

## 🗂️ Estructura del proyecto
El proyecto sigue un **patrón SoC (Separation of Concerns)**, donde cada dominio tiene su propio espacio con responsabilidades bien definidas:

Nota: Cada dominio lleva los siguientes archivos: routers, services, models, schemas y exceptions

```plaintext
api/src/
   ├─ order/ # Manejo de órdenes
   │ ├─ event/        # Flujo de eventos con Kafka
   │ │   ├─ consumer.py # Consumer para escuchar mensajes de Kafka
   │ │   └─ producer.py # Producer para publicar mensajes en Kafka
   │ └─ proto/        # Definición de contratos y tipos
   │     ├─ order_events_pb2.py # Esquemas de eventos de órdenes
   │     └─ order_events_pb2.pyi # Definición de tipos relacionados
   │ ├─ routers.py # Endpoints de API para órdenes
   │ ├─ services.py # Lógica de negocio de órdenes
   │ ├─ schemas.py # Esquemas Pydantic para validaciones
   │ ├─ models.py # Modelos de base de datos
   │ └─ exceptions.py # Excepciones personalizadas

   ├─ product/ # Manejo de productos
   ├─ inventory/ # Manejo del inventario
   ├─ health/ # Endpoints de health-check

   ├─ config/ # Configuración global de base de datos y entorno
   └─ main.py # Punto de entrada de la aplicación
.env # Archivo de variables de entorno (Debe crearse)
.env.example # Ejemplo de archivo de variables de entorno
```

## ⚙️ Configuración de variables de entorno

Se utiliza un archivo **.env** en el root del proyecto para parametrizar la aplicación.

### 📄 Ejemplo de `.env`
```bash
# App name
APP_NAME=E-commerce Orders Service

# Frontend
FRONTEND_BASE_URL=url_front

# Security
BACKEND_CORS_ORIGIN='["*"]'

# PostgreSQL
POSTGRES_DB=ecommerce_inventory
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_HOST_AUTH_METHOD=trust
POSTGRES_PORT=5432

# MongoDB
MONGO_INITDB_ROOT_USERNAME=user
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_INITDB_DATABASE=ecommerce_orders
MONGO_PORT=27017
MONGO_URI=mongodb://user:password@mongodb:27017

# Zookeeper
ZOOKEEPER_CLIENT_PORT=2181
ZOOKEEPER_TICK_TIME=2000

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_BROKER_ID=1
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_INTERNAL://kafka:29092
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT_INTERNAL
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
KAFKA_AUTO_CREATE_TOPICS_ENABLE=true
KAFKA_NUM_PARTITIONS=3
KAFKA_DEFAULT_REPLICATION_FACTOR=1
KAFKA_PORT_1=9092
KAFKA_PORT_2=9101

# Schema Registry
SCHEMA_REGISTRY_HOST_NAME=schema-registry
SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=kafka:29092
SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8081
SCHEMA_REGISTRY_PORT=8081
```

## 📌 Nota importante
Los contenedores **no se conectan con `localhost`**, sino por **nombre de servicio en Docker Compose** (`postgres`, `mongodb`, `kafka`, etc.).  
Esto garantiza que los servicios puedan resolverse correctamente dentro de la red interna de Docker.

---

## 🛠️ Requisitos
- Docker Desktop  
- Docker Compose  

---

## 🔧 Comandos principales

### Construir imágenes desde cero
```bash
docker-compose build --no-cache
```

### Ejecutar la aplicación
```bash
docker-compose up 
```

## 📖 Documentación de la API

La documentación estará disponible en:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## Flujo de arquitectura
![Diagrama de arquitectura](resources/flow_architecture_ecommerce.png)


## Flujo del Sistema
1. API REST recibe la orden
2. Validación inicial de datos e inventario
3. Publicar evento a Kafka para procesamiento asíncrono
4. Consumer de Kafka procesa la orden:
   - Simula procesamiento de pago
   - Actualiza inventario (PostgreSQL)
   - Guarda orden completa (MongoDB)



## Casos Edge suplidos
- Inventario insuficiente
- Productos inexistentes
- Fallos de pago simulado
- Órdenes duplicadas (idempotencia)


