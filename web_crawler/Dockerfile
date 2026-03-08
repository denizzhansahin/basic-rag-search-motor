FROM python:3.11-slim

# 1. KATMAN: Sistem Bağımlılıkları (Nadiren değişir, en ağır katmandır)
# Docker bunu bir kez kurar ve cache'e alır.
# Sistem bağımlılıkları (Chromium'un Docker'da çalışması için gereken tüm paketler)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. KATMAN: Python Kütüphaneleri (Sadece requirements.txt değişince güncellenir)
# 'COPY . .' yerine önce sadece requirements kopyalıyoruz
COPY web_crawler/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3. KATMAN: Proje Kodları (Her build'de güncellenir ama üstteki katmanları bozmaz)
# Context ../ olduğu için dosyaları klasör yapısıyla alıyoruz
COPY . .

# Ortam değişkenleri
ENV PYTHONPATH="/app:/app/web_crawler"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/
ENV PYTHONUNBUFFERED=1

# Başlatma scriptine yetki ver
RUN chmod +x /app/web_crawler/start_crawler.sh

EXPOSE 8501

# Çalıştırılacak komut (Yol düzeltildi)
CMD ["/app/web_crawler/start_crawler.sh"]