# API REST - Extracción de resumen y entidades de un texto

El proyecto es una API construída con FastAPI que expone endpoints para guardar en memoria, resumir un texto y ver el listado de textos. La API expone los siguientes endpoints: 
- POST /api/v1/document (Recibe el texto a traves de texto plano)
- POST /api/v1/document/{id}/analyze (Hace el análisis del texto y retorna el resumen y las entidades principales extraídas.)
- GET /api/v1/queries (Lista los textos cargados en memoria, es necesario enviar un token válido para acceder.)
- POST /api/v1/login (Retorna un token válido para un minuto.)

## Variables de entorno:
Para el funcionamiento del proyecto es necesario asignar las variables SECRET_JWT_KEY, JWT_ALGORITHM, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY y AWS_DEFAULT_REGION. El archivo env.sample muestra un ejemplo.

## Ejecución local:

Se recomienda primero la creación de un entorno virtual.

python -m venv env

Activar el entorno virtual:

.\env\Scripts\activate (para windows)

Instalar las dependencias:

pip install .

Ejecutar el Api:

python .\src\api_handler.py 

## Ejecución con Docker:

Hacer la construcción de la imagen de Docker:

docker build -t resumen-api .

Ejecutar un contenedor:

docker run -p 8000:8000 --env-file .env resumen-api

## Ejecución con Docker composer:

Ejecutar el comando:

docker-compose up

# Video:

A continuación se comparte el link del video en el que se explica el código y su uso:

https://drive.google.com/file/d/1sHtl07CpZnrfinl1G8052yX8qGZLZ7eW/view?usp=sharing
