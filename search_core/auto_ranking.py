from datetime import datetime, date

def freshness_boost(results):
    now = datetime.now()
    for r in results:
        item_date = r.get('date')
        if not item_date:
            continue
            
        try:
            # Gelen veri datetime.date objesi ise datetime'a çevir
            if isinstance(item_date, date) and not isinstance(item_date, datetime):
                item_date = datetime.combine(item_date, datetime.min.time())
            # Gelen veri string ise datetime objesine dönüştür (YYYY-MM-DD formatı varsayımı)
            elif isinstance(item_date, str):
                # Sadece ilk 10 karakteri alıp parse edelim "2024-05-12"
                item_date = datetime.strptime(item_date[:10], "%Y-%m-%d")

            age_days = (now - item_date).days
            boost = max(0, 1 - (age_days / 365))  # 1 yıl üzeri içeriklerde boost sıfırlanır
            r['score'] += boost * 0.1
        except Exception as e:
            continue # Tarih parse edilemezse skoru değiştirme
            
    return sorted(results, key=lambda x: x['score'], reverse=True)