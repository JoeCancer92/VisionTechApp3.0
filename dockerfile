# Dockerfile para la aplicación VisionTechApp

# Usa una imagen base ligera de Python
FROM python:3.8-slim

# Mantener el sistema actualizado e instalar cmake y demás herramientas necesarias
RUN apt-get update && \
    apt-get install -y cmake g++ wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requerimientos al contenedor
COPY requirements.txt /app/

# Actualizar pip e instalar las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el resto del código al contenedor
COPY . /app

# Exponer el puerto que la aplicación usará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
