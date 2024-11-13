#!/bin/bash

# Actualizar los paquetes e instalar CMake
echo "Instalando CMake..."
apt-get update && apt-get install -y cmake

# Confirmar la instalación
echo "Instalación de CMake completa"
