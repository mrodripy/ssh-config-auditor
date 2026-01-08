# Usa una imagen base oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos primero (para aprovechar la cache de Docker)
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY src/ ./src/
COPY configs/ ./configs/
COPY samples/ ./samples/

# Hace del script de auditoría el punto de entrada por defecto
ENTRYPOINT ["python", "./src/ssh_audit.py"]

# Define un volumen por defecto para montar configuraciones SSH del host
VOLUME ["/data"]

# Comando por defecto: mostrar ayuda si no se dan argumentos
CMD ["--help"]
