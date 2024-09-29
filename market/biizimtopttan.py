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
    CREATE TABLE IF NOT EXISTS bizim_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255),
        price DECIMAL(10, 2),
        image BLOB
    );
    """)

    # Market URL'lerini tanımlayın
    market_urls = [
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin",
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin?pagenumber=2&paginationType=10",
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin?pagenumber=3&paginationType=10",
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin?pagenumber=4&paginationType=10",
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin?pagenumber=5&paginationType=10",
        "https://www.bizimtoptan.com.tr/sivi-yag-margarin?pagenumber=6&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=2&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=3&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=4&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=5&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=6&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=7&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=8&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=9&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=10&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=11&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=12&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=13&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=14&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=15&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=16&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=17&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=18&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=19&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=20&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=21&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=22&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=23&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=24&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=25&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=26&paginationType=10",
        "https://www.bizimtoptan.com.tr/temel-gida?pagenumber=27&paginationType=10",
        "https://www.bizimtoptan.com.tr/atistirmalik",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=2&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=3&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=4&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=5&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=6&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=7&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=8&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=9&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=10&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=11&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=12&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=14&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=15&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=16&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=17&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=18&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=19&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=20&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=21&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=22&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=23&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=24&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=25&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=26&paginationtype=10",
        "https://www.bizimtoptan.com.tr/atistirmalik?paginationType=10%2C10%2C10&pagenumber=27&paginationtype=10",
        "https://www.bizimtoptan.com.tr/icecek",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=2&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=3&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=4&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=5&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=6&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=7&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=8&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=9&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=10&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=11&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=12&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=13&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=14&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=15&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=16&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=17&paginationType=10",
        "https://www.bizimtoptan.com.tr/icecek?pagenumber=18&paginationType=10",
        "https://www.bizimtoptan.com.tr/et-urunleri-ve-sarkuteri",
        "https://www.bizimtoptan.com.tr/temizlik",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=2&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=3&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=4&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=5&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=6&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=7&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=8&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=9&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=10&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=11&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=12&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=13&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=14&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=15&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=16&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=17&paginationType=10",
        "https://www.bizimtoptan.com.tr/temizlik?pagenumber=18&paginationType=10",


       
    ]

    # Ürün bilgilerini toplama işlemi
    for market_url in market_urls:
        try:
            # Marketin ürün sayfasını açma
            driver.get(market_url)

            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-list-container"))
            )

            # Sayfanın altına doğru scroll yap
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # İçeriğin yüklenmesi için bekleme süresi

            # Ürün kartlarını seçme
            product_cards = driver.find_elements(By.CSS_SELECTOR, "div.product-box-container")

            for card in product_cards:
                # Ürün adını alma
                try:
                    product_name = card.find_element(By.CSS_SELECTOR, "h2.productbox-name").text
                except Exception as e:
                    product_name = "Ürün adı bulunamadı"
                    print(f"Error retrieving product name: {e}")

                # Fiyatı bulmaya çalış
                try:
                    product_price = card.find_element(By.CSS_SELECTOR, "p.product-price").text
                    product_price = preprocess_price(product_price)
                except Exception as e:
                    product_price = None
                    print(f"Error retrieving product price: {e}")

                # Ürün resmini alma
                try:
                    image_element = card.find_element(By.CSS_SELECTOR, "div.product-box-image-container img")
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
                INSERT INTO bizim_products (product_name, price, image) 
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
