FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY pyproject.toml .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copiar código fuente
COPY src/ ./src/

# Agregar el directorio src al PYTHONPATH
ENV PYTHONPATH=/app/src

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "-m", "uvicorn", "api_handler:app", "--host", "0.0.0.0", "--port", "8000"]
