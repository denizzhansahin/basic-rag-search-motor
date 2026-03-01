import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def site_haritasi_cikar(baslangic_url, max_sayfa=20):
    """
    Belirtilen bir web sitesine girer ve o domaine ait alt sayfaları bulur.
    max_sayfa: Botun sonsuza kadar çalışmasını engellemek için bir güvenlik sınırı.
    """
    
    # 1. Kuyruk ve Ziyaret Edilenler Seti
    ziyaret_edilecekler = [baslangic_url]
    ziyaret_edilenler = set()
    bulunan_gecerli_linkler = set()
    
    # Başlangıç domainini alıyoruz (Örn: shiftdelete.net). 
    # Botun dışarıya (başka sitelere) kaçmasını engellemek için.
    ana_domain = urlparse(baslangic_url).netloc
    
    print(f"🕷️ Web Crawler '{ana_domain}' üzerinde çalışmaya başlıyor...\n")

    while ziyaret_edilecekler and len(ziyaret_edilenler) < max_sayfa:
        # Kuyruğun en başındaki linki al
        suanki_url = ziyaret_edilecekler.pop(0)
        
        # Eğer bu sayfaya daha önce girdiysek atla
        if suanki_url in ziyaret_edilenler:
            continue
            
        try:
            print(f"Taraniyor: {suanki_url}")
            # Sayfayı indir (Timeout ekliyoruz ki site yanıt vermezse bot takılmasın)
            cevap = requests.get(suanki_url, timeout=5)
            
            # Sadece başarılı yanıtları (200 OK) işle
            if cevap.status_code == 200:
                soup = BeautifulSoup(cevap.text, "html.parser")
                ziyaret_edilenler.add(suanki_url)
                
                # Sayfadaki tüm <a> (link) etiketlerini bul
                for a_etiketi in soup.find_all("a", href=True):
                    ham_link = a_etiketi["href"]
                    
                    # Göreceli linkleri (Örn: /haber/test) tam linke çevir
                    tam_link = urljoin(suanki_url, ham_link)
                    
                    # URL'nin sonundaki gereksiz çapa ve parametreleri temizle (Örn: #yorumlar)
                    temiz_link = tam_link.split("#")[0].split("?")[0]
                    
                    # FİLTRE: Link bizim ana domainde mi? Ve daha önce bulmadığımız bir link mi?
                    if ana_domain in urlparse(temiz_link).netloc:
                        # Resim, PDF veya mailto linki değilse listeye ekle
                        if not temiz_link.endswith(('.jpg', '.png', '.pdf', '.zip')) and "mailto:" not in temiz_link:
                            if temiz_link not in bulunan_gecerli_linkler and temiz_link not in ziyaret_edilenler:
                                ziyaret_edilecekler.append(temiz_link)
                                bulunan_gecerli_linkler.add(temiz_link)
            
            # Sunucuyu yormamak ve ban yememek için ufak bir bekleme süresi
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Bağlantı hatası ({suanki_url}): {e}")

    print(f"\n✅ Tarama Tamamlandı! Toplam {len(bulunan_gecerli_linkler)} adet alt sayfa bulundu.")
    return list(bulunan_gecerli_linkler)

# Test Etmek İçin:
linkler = site_haritasi_cikar("https://shiftdelete.net", max_sayfa=10)
for link in linkler:
   print(link)