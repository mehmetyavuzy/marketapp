from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# EdgeDriver'ın yolunu belirtin
edge_driver_path = 'C:/Users/yavuz/Desktop/market/msedgedriver.exe'

# Edge seçeneklerini ayarlama
edge_options = Options()
edge_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat

# EdgeDriver servisini başlatma
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# Market URL'lerini tanımlayın
market_urls = [
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=2&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=1&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=4&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=5&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=6&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=7&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=8&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=9&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=10&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=11&sirala=onerilenler",
    "https://www.migros.com.tr/hemen/temel-gida-c-1129c?sayfa=12&sirala=onerilenler",
    
    
    # Buraya diğer market URL'lerini ekleyin
]

try:
    for market_url in market_urls:
        # Marketin ürün sayfasını açma
        driver.get(market_url)

        # Sayfanın yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sm-list-page-item"))
        )

        # Scroll yaparak sayfanın altına doğru in
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # İçeriğin yüklenmesi için bekleme süresi

        # Ürün kartlarını seçme
        product_cards = driver.find_elements(By.CSS_SELECTOR, "sm-list-page-item")

        for card in product_cards:
            # Ürün adını alma
            try:
                product_name = card.find_element(By.CLASS_NAME, "product-name").text
            except:
                product_name = "Ürün adı bulunamadı"

            # Fiyatı bulmaya çalış (XPath kullanarak)
            try:
                product_price = card.find_element(By.CLASS_NAME, "amount").text
            except:
                product_price = "Fiyat bulunamadı"

            print(f" Ürün Adı: {product_name} - Fiyat: {product_price}")

finally:
    # Tarayıcıyı kapatma
    driver.quit()
