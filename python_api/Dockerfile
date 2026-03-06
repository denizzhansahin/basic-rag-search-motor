FROM python:3.10-slim

WORKDIR /app

# 1. Adım: Sistem paketlerini kur (Bu katman neredeyse hiç değişmez, hep CACHED kalır)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 2. Adım: SADECE requirements.txt dosyasını kopyala
# Burası kritik! Kodun değişse bile requirements değişmediği sürece burayı atlar.
COPY python_api/requirements.txt ./python_api/

# 3. Adım: Kütüphaneleri kur
RUN pip install --no-cache-dir -r ./python_api/requirements.txt

# 4. Adım: ŞİMDİ tüm kodları kopyala
# Artık kodda istediğin kadar değişiklik yap, yukarıdaki 3 adım saniyeler içinde 'CACHED' diye geçecek.
COPY . .

CMD ["python", "python_api/worker_docker.py"]