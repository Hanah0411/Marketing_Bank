# Imagen base
FROM python:3.11-slim

# Carpeta de trabajo
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar proyecto
COPY . .

# Exponer puertos de FastAPI (8000) y Dash (8050)
EXPOSE 8000 8050

# Comando para iniciar ambos servicios
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python -m app.dashboards.dashboard --host 0.0.0.0 --port 8050"]
