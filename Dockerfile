# Dockerfile per Google Maps Scraper
FROM python:3.11-slim

# Installa dipendenze sistema per Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    libxss1 \
    libgconf-2-4 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Imposta directory di lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copia il codice
COPY . .

# Comando di avvio
CMD ["python3", "main.py"]
