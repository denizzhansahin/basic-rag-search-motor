#!/bin/bash

# Debug için: Dosyalar ve değişkenler ne durumda?
echo "📍 Mevcut Dizin: $(pwd)"
echo "🖥️ İşlemci Modu: $CPU_MODE"
which chromium # Chrome yüklü mü?

echo "🚀 Space Teknopoli Web Crawler Başlatılıyor..."

# Dosyaların olduğu klasöre git
cd /app/web_crawler

# 1. Site Manager'ı arka planda başlat
python3 site_manager.py &

# 2. Worker'ı başlat
if [ "$CPU_MODE" = "high" ]; then
    echo "⚡ M4 Gücü Aktif: redis_queue_worker.py çalışıyor..."
    python3 redis_queue_worker.py
else
    echo "🐢 Düşük Güç Modu: redis_queue.py çalışıyor..."
    python3 redis_queue.py
fi