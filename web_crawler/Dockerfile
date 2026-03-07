FROM python:3.11-slim

# Sistem bağımlılıklarını kur
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıkları kopyala ve kur
# (Klasöründe requirements.txt olduğunu varsayıyorum, yoksa streamlit ve redis ekle)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# PYTHONPATH ayarını Docker seviyesinde yapalım
ENV PYTHONPATH="/app:/app/web_crawler"

# Başlatma scriptini kopyala ve yetki ver
COPY start_crawler.sh /start_crawler.sh
RUN chmod +x /start_crawler.sh

# Streamlit portu
EXPOSE 8501

# Başlatma scriptini çalıştır
CMD ["/start_crawler.sh"]