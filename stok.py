import requests
from bs4 import BeautifulSoup

url = "https://konfuse.shop/the-wolf-t-shirt"
TELEGRAM_TOKEN = "8433150649:AAFu00v4e3MR4f2DRckO4jZTZbOaBwA8G8E"
TELEGRAM_CHAT_ID = "6031644473"

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
            print(f"Siteye erişilemedi: {sayfa.status_code}")
            return
            
        soup = BeautifulSoup(sayfa.content, "html.parser")
        secenekler = soup.find_all("option")
        istenen_stokta = False
        
        for secenek in secenekler:
            metin = secenek.text.lower()
            siyah_mi = "siyah" in metin or "black" in metin
            beden_mi = "l" in metin or "xl" in metin
            
            if siyah_mi and beden_mi:
                if "yok" not in metin and "tükendi" not in metin and "sold" not in metin and "out" not in metin:
                    if not secenek.has_attr('disabled'):
                        istenen_stokta = True
                        break

        if istenen_stokta:
            mesaj = "🚨 KANKA KOŞ! Siyah renk L veya XL beden STOĞA GİRDİ! 🚨\n\nLink: https://konfuse.shop/the-wolf-t-shirt"
            telegram_mesaj_gonder(mesaj)
            print("Stok bulundu, Telegram'a uçuruldu!")
        else:
            print("Siyah renk L/XL hala tükenmiş durumda.")
            
    except Exception as e:
        print("Hata oluştu:", e)

# Döngü yok, direkt tek seferlik çalıştırıyoruz
stok_kontrol_siyah_html()