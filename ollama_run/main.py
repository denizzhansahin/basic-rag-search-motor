from ollama_rag_read import soru_sor

def main():
    print("--- RAG Sistemine Hoş Geldiniz ---")

    # Geçmişi artık bir metin olarak değil, liste olarak tutuyoruz.
    sohbet_gecmisi_listesi = []
    
    # Modelin hatırlamasını istediğimiz MAKSİMUM geçmiş soru-cevap sayısı.
    # 3 veya 4 idealdir. Çok artırırsan modelin kafası tekrar karışabilir.
    MAX_GECMIS_SAYISI = 30 

    # Soru - Cevap Döngüsü
    while True:
        kullanici_sorusu = input("\nSorunuzu yazın (Çıkmak için 'q' tuşlayın): ")
        
        if kullanici_sorusu.lower() == 'q':
            print("Çıkış yapılıyor...")
            break
            
        # Listede tuttuğumuz son N mesajı alıp tek bir metin (string) haline getiriyoruz.
        # [-MAX_GECMIS_SAYISI:] ifadesi listenin sadece son 3 elemanını alır.
        aktif_gecmis_metni = "".join(sohbet_gecmisi_listesi[-MAX_GECMIS_SAYISI:])
        
        # soru_sor fonksiyonuna bu filtrelenmiş taze geçmişi gönderiyoruz
        cevap = soru_sor(
            soru=kullanici_sorusu, 
            sohbet_gecmisi=aktif_gecmis_metni, 
            collection_name="ollama_my_rag_collection"
        )
        
        print("\n🤖 Gemma'nın Cevabı:")
        print("-" * 30)
        print(cevap)
        print("-" * 30)

        # Döngünün sonunda, mevcut soruyu ve cevabı yeni bir blok olarak listeye ekliyoruz
        yeni_etkilesim = f"Kullanıcı: {kullanici_sorusu}\nAsistan: {cevap}\n\n"
        sohbet_gecmisi_listesi.append(yeni_etkilesim)

if __name__ == "__main__":
    main()