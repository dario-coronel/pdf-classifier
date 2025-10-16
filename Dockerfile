# Dockerfile para PDF Classifier (Flask + ML)
FROM python:3.13-slim

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y gcc tesseract-ocr poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Flask
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]
