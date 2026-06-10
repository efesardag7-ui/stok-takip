import requests
from bs4 import BeautifulSoup
import time

# Orijinal ürün linki
url = "https://konfuse.shop/the-wolf-t-shirt"

TELEGRAM_TOKEN = "8433150649:AAFu00v4e3MR4f2DRckO4jZTZbOaBwA8G8E"
TELEGRAM_CHAT_ID = "-1004071540524"

def telegram_mesaj_gonder(mesaj):
    try:
        url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj}
        requests.post(url_telegram, data=payload)
    except:
        pass

def stok_kontrol_siyah_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        sayfa = requests.get(url, headers=headers)
        
        if sayfa.status_code != 200:
            print(f"Siteye erişilemedi (Hata Kodu: {sayfa.status_code}), 5 dk sonra tekrar denenecek...")
            return False
            
        soup = BeautifulSoup(sayfa.content, "html.parser")
        
        # Shopify sitelerinde arka planda çalışan ve kesin stok durumunu barındıran select/option listesine bakıyoruz
        secenekler = soup.find_all("option")
        
        istenen_stokta = False
        
        for secenek in secenekler:
            metin = secenek.text.lower()
            # Örnek Shopify yapısı: "Siyah / L - Stokta Yok" veya "Siyah / L"
            
            siyah_mi = "siyah" in metin or "black" in metin
            beden_mi = "l" in metin or "xl" in metin
            
            # Eğer seçeneğin içinde "siyah" ve "l/xl" geçiyor üstüne "stokta yok", "sold" veya "tükendi" GEÇMİYORSA stok gelmiştir.
            if siyah_mi and beden_mi:
                if "yok" not in metin and "tükendi" not in metin and "sold" not in metin and "out" not in metin:
                    # Ayrıca bazı siteler görünmez seçenleri korur, seçeneğin pasif (disabled) olmadığına emin olalım
                    if not secenek.has_attr('disabled'):
                        istenen_stokta = True
                        break

        if istenen_stokta:
            mesaj = "🚨 KANKA KOŞ! Siyah renk L veya XL beden STOĞA GİRDİ! 🚨\n\nLink: https://konfuse.shop/the-wolf-t-shirt"
            telegram_mesaj_gonder(mesaj)
            return True
        else:
            print("Kontrol başarılı: Siyah renk L/XL seçeneği hala tükenmiş görünüyor... Nöbete devam.")
            return False
            
    except Exception as e:
        print("Sayfa taranırken bir sorun yaşandı, 5 dk sonra tekrar denenecek:", e)
        return False

# Başlangıç
print("🤖 Siyah L/XL HTML botu devrede!")
telegram_mesaj_gonder("🤖 Siyah renk L/XL güvenli takip botu başarıyla başlatıldı!")

while True:
    if stok_kontrol_siyah_html():
        print("Bot görevini tamamladı ve durduruldu.")
        break
    time.sleep(600)