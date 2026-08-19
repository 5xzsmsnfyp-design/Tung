from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://google.com")
print("Site Başlığı:", driver.title)
driver.quit()
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("--> Bot başlatılıyor...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("--> Hedef siteye gidiliyor...")
driver.get("https://google.com")

print("--> Sayfa başlığı alındı:", driver.title)

# Örnek döngü / işlem adımları
for i in range(1, 4):
    print(f"--> İşlem adımı {i} yapılıyor...")
    time.sleep(1)

print("--> İşlem tamamlandı, kapatılıyor.")
driver.quit()
