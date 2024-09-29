from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector
from urllib.request import urlopen, Request

edge_driver_path = 'C:/Users/yavuz/Desktop/market/msedgedriver.exe'

# Edge seçeneklerini ayarlama
edge_options = Options()
edge_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat

# EdgeDriver servisini başlatma
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# MySQL bağlantısı
db_config = {
    'user': 'root',  
    'password': ''
    'host': 'localhost',
    'database': 'market_data'
}

def preprocess_price(price_str):
    """Fiyatı DECIMAL formatına uygun şekilde dönüştür."""
    price_str = price_str.replace('TL', '').strip()
    price_str = price_str.replace(',', '.')
    try:
        return float(price_str)
    except ValueError:
        return None

# MySQL bağlantısını açma
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Veritabanı tablosu oluşturma (eğer yoksa)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS migros_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255),
        price DECIMAL(10, 2),
        image BLOB
    );
    """)

    # Market URL'lerini tanımlayın
    market_urls = [
        "https://www.migros.com.tr/hemen/camasir-c-112b1?sayfa=1",
        "https://www.migros.com.tr/hemen/camasir-c-112b1?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/camasir-c-112b1?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bulasik-c-112b2?sayfa=1",
        "https://www.migros.com.tr/hemen/bulasik-c-112b2?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/mutfak-c-112b3?sayfa=1",
        "https://www.migros.com.tr/hemen/bulasik-c-112b2?sayfa=1",
        "https://www.migros.com.tr/hemen/mutfak-c-112b3?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/temizlik-c-112b4?sayfa=1",
        "https://www.migros.com.tr/hemen/temizlik-c-112b4?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/temizlik-c-112b4?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/temizlik-c-112b4?sayfa=4&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/sabun-c-112b5?sayfa=1",
        "https://www.migros.com.tr/hemen/su-c-11254?sayfa=1",
        "https://www.migros.com.tr/hemen/maden-suyu-c-11255?sayfa=1",
        "https://www.migros.com.tr/hemen/gazli-icecek-c-1126f?sayfa=1",
        "https://www.migros.com.tr/hemen/gazli-icecek-c-1126f?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/gazli-icecek-c-1126f?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/meyve-suyu-c-11270?sayfa=1",
        "https://www.migros.com.tr/hemen/meyve-suyu-c-11270?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/meyve-suyu-c-11270?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/soguk-kahve-c-11273?sayfa=1",
        "https://www.migros.com.tr/hemen/enerji-icecegi-c-11272?sayfa=1",
        "https://www.migros.com.tr/hemen/soguk-cay-c-11271?sayfa=1",
        "https://www.migros.com.tr/hemen/soguk-cay-c-11271?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/makarna-c-1129e?sayfa=1&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/makarna-c-1129e?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/makarna-c-1129e?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bakliyat-c-1129d?sayfa=1",
        "https://www.migros.com.tr/hemen/bakliyat-c-1129d?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bakliyat-c-1129d?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=1&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=4&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=5&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=6&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=7&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=8&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=9&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=10&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=11&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=12&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=13&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=14&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=15&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=16&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=17&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=18&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=19&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=20&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=21&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=22&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=23&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/atistirmalik-c-1125b?sayfa=24&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bebek-c-112a7",
        "https://www.migros.com.tr/hemen/bebek-c-112a7?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bebek-c-112a7?sayfa=3&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bebek-c-112a7?sayfa=4&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/dondurma-c-11280?sayfa=2&sirala=onerilenler",
        "https://www.migros.com.tr/hemen/bebek-c-112a7?sayfa=2&sirala=onerilenler",


    ]

    # Ürün bilgilerini toplama işlemi
    for market_url in market_urls:
        try:
            # Marketin ürün sayfasını açma
            driver.get(market_url)

            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sm-list-page-item"))
            )

            # Sayfanın altına doğru scroll yap
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # İçeriğin yüklenmesi için bekleme süresi

            # Ürün kartlarını seçme
            product_cards = driver.find_elements(By.CSS_SELECTOR, "sm-list-page-item")

            for card in product_cards:
                # Ürün adını alma
                try:
                    product_name = card.find_element(By.CSS_SELECTOR, "a#product-name").text
                except Exception as e:
                    product_name = "Ürün adı bulunamadı"
                    print(f"Error retrieving product name: {e}")

                # Fiyatı bulmaya çalış
                try:
                    product_price = card.find_element(By.CSS_SELECTOR, "fe-product-price").text
                    product_price = preprocess_price(product_price)
                except Exception as e:
                    product_price = None
                    print(f"Error retrieving product price: {e}")

                # Ürün resmini alma
                try:
                    image_element = card.find_element(By.CSS_SELECTOR, "img")
                    image_url = image_element.get_attribute("src")

                    # User-Agent başlığı ekleyerek görüntüyü indirme
                    req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urlopen(req) as response:
                        image_data = response.read()
                except Exception as e:
                    image_data = None
                    print(f"Error retrieving product image: {e}")

                # Veriyi MySQL veritabanına ekleme
                cursor.execute("""
                INSERT INTO migros_products (product_name, price, image) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    price = VALUES(price),
                    image = VALUES(image)
                """, (product_name, product_price, image_data))
                connection.commit()

                print(f"Ürün Adı: {product_name} - Fiyat: {product_price}")

        except Exception as e:
            print(f"Error processing URL {market_url}: {e}")

finally:
    # Veritabanı bağlantısını kapatma
    if connection.is_connected():
        cursor.close()
        connection.close()
    
    # Tarayıcıyı kapatma
    driver.quit()

