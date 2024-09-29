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
    'password': '',
    'host': 'localhost',
    'database': 'market_data'
}

def preprocess_price(price_str):
    """Fiyatı DECIMAL formatına uygun şekilde dönüştür."""
    price_str = price_str.replace('₺', '').replace('TL', '').strip()
    price_str = price_str.replace(',', '.')
    try:
        return float(price_str)
    except ValueError:
        return None

# MySQL bağlantı
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Veritabanı tablosu oluşturma (eğer yoksa)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sok_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255),
        price DECIMAL(10, 2),
        image BLOB
    );
    """)

    # Market URL'lerini tanımlayın
    market_urls = [
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=1",
       "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=2",
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=3",
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=4",
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=5",
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=6",
        "https://www.sokmarket.com.tr/sut-ve-sut-urunleri-c-460?page=7",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=2",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=3",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=4",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=5",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=6",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=7",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=8",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=9",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=10",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=11",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=12",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=11",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=13",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=14",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=15",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=16",
        "https://www.sokmarket.com.tr/kisisel-bakim-ve-kozmetik-c-20395?page=17",
        "https://www.sokmarket.com.tr/temizlik-c-20647",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=2",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=3",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=4",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=5",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=6",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=7",
        "https://www.sokmarket.com.tr/temizlik-c-20647?page=8",
        "https://www.sokmarket.com.tr/icecek-c-20505",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=2",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=3",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=4",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=5",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=6",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=7",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=8",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=9",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=10",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=11",
        "https://www.sokmarket.com.tr/icecek-c-20505?page=12",
        "https://www.sokmarket.com.tr/kagit-urunler-c-20875",
        "https://www.sokmarket.com.tr/kagit-urunler-c-20875?page=2",
        "https://www.sokmarket.com.tr/dondurma-c-31102",
        "https://www.sokmarket.com.tr/dondurma-c-31102?page=2",
        "https://www.sokmarket.com.tr/dondurma-c-31102?page=3",
        "https://www.sokmarket.com.tr/dondurma-c-31102?page=4",
        "https://www.sokmarket.com.tr/dondurulmus-urunler-c-1550",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=2",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=3",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=4",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=5",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=6",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=7",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=8",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=9",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=10",
        "https://www.sokmarket.com.tr/atistirmaliklar-c-20376?page=11",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=1",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=2",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=3",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=4",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=5",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=6",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=1",
        "https://www.sokmarket.com.tr/anne-bebek-ve-cocuk-c-20634?page=1",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=2",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=3",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=4",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=5",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=6",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=7",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=8",
        "https://www.sokmarket.com.tr/yemeklik-malzemeler-c-1770?page=9",
  

    ]

    # Ürün bilgilerini toplama işlemi
    for market_url in market_urls:
        try:
            # Marketin ürün sayfasını açma
            driver.get(market_url)

            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.CProductCard-module_productCardWrapper__okAmT"))
            )

            # Sayfanın altına doğru scroll yap
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # İçeriğin yüklenmesi için bekleme süresi

            # Ürün kartlarını seçme
            product_cards = driver.find_elements(By.CSS_SELECTOR, "div.CProductCard-module_productCardWrapper__okAmT")

            for card in product_cards:
                # Ürün adını alma
                try:
                    product_name = card.find_element(By.CSS_SELECTOR, "h2.CProductCard-module_title__u8bMW").text
                except Exception as e:
                    product_name = "Ürün adı bulunamadı"
                    print(f"Error retrieving product name: {e}")

                # Fiyatı bulmaya çalış
                try:
                    # Fiyatı almak için doğru CSS seçiciyi kullanıyorum
                    price_element = card.find_element(By.CSS_SELECTOR, "span.CPriceBox-module_price__bYk-c")
                    product_price = price_element.text
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
                INSERT INTO sok_products (product_name, price, image) 
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
