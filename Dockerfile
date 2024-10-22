# Gunakan image Python sebagai dasar
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install sqlite-web, sqlite3, dan supervisord
RUN apt-get update && apt-get install -y \
    sqlite3 \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Buat direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt dan instal dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh konten proyek ke dalam container
COPY . /app

# Salin konfigurasi supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port untuk sqlite-web (misalnya, port 8080)
EXPOSE 8080

# Jalankan supervisord sebagai perintah utama
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
