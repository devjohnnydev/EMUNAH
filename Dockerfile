# Dockerfile para deploy no Railway - Projeto Flask Python
FROM python:3.11-slim

# Instalar dependências do sistema para WeasyPrint e outras libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    libgirepository1.0-dev \
    gir1.2-pango-1.0 \
    fonts-liberation \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas requirements primeiro (para cache de camadas)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Criar diretórios de upload se necessário
RUN mkdir -p static/uploads/quotes static/uploads/prints

# Expor porta (Railway usa variável PORT)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/login || exit 1

# Comando de inicialização - usa gunicorn diretamente com main:app
CMD gunicorn main:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 --access-logfile - --error-logfile -
