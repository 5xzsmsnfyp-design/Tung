import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("==========================================")
print("--> Bot başlatılıyor...")

# 1. GitHub Actions'tan gelen dosya adını al (Varsayılan: combo.txt)
dosya_yolu = os.getenv("GIRILEN_DOSYA", "combo.txt")
print(f"--> Kullanılacak dosya: {dosya_yolu}")

# 2. Chrome Headless (Arka Plan) Ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# 3. Tarayıcıyı Çalıştır
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 4. Dosyayı Okuma ve İşleme
try:
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        satirlar = f.readlines()
    
    print(f"--> Toplam {len(satirlar)} adet veri okundu. İşlem başlıyor...\n")

    for satir in satirlar:
        veri = satir.strip()
        if not veri:
            continue
        
        print(f"[KONTROL EDİLİYOR]: {veri}")
        
        # --- BURAYA KENDİ OTOMASYON / CHECKER ADIMLARINI EKLEYECEKSİN ---
        driver.get("https://google.com")
        time.sleep(1) # Sitede işlem yapma süresi
        # -----------------------------------------------------------------

except FileNotFoundError:
    print(f"[HATA] '{dosya_yolu}' adında bir dosya bulunamadı! Lütfen repository'ye ekleyin.")

# 5. Ekran Görüntüsü Al ve Kapat
driver.save_screenshot("ekran.png")
print("\n--> Ekran görüntüsü kaydedildi (ekran.png).")
driver.quit()
print("--> Bot işlemi tamamlandı.")
print("==========================================")
