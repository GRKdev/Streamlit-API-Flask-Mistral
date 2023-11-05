# Dockerfile
FROM python:3.11.5-slim-bullseye

# Copia tu aplicación al contenedor
COPY . /app
WORKDIR /app

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto 8080
EXPOSE 8080

# Comando para ejecutar gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--reload", "main:app"]
