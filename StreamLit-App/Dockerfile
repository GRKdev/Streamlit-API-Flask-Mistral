FROM python:3.11-slim-buster
ENV HOST=0.0.0.0
ENV LISTEN_PORT 8083
EXPOSE 8082

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt


CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8083"]
