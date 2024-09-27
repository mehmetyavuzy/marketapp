import requests
from bs4 import BeautifulSoup
import mysql.connector

# Web scraping işlemi
url = 'https://www.nefisyemektarifleri.com/tarifler/'  # Kendi hedef sayfanızın URL'si ile değiştirin
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Tarifleri ayrıştırma
recipes = []
for item in soup.find_all('div', class_='recipe'):  # HTML sınıflarını sayfanıza göre ayarlayın
    name = item.find('h2').text
    ingredients = item.find('ul', class_='ingredients').text
    instructions = item.find('div', class_='instructions').text
    recipes.append({
        'name': name,
        'ingredients': ingredients,
        'instructions': instructions
    })

# MySQL veritabanına bağlanma
try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mehmet69436943',  # Kendi MySQL kullanıcı adınız ve şifreniz ile değiştirin
        database='recipes_db'
    )
    
    cursor = db.cursor()

    # Tarifleri MySQL'e kaydetme
    for recipe in recipes:
        sql = "INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)"
        val = (recipe['name'], recipe['ingredients'], recipe['instructions'])
        cursor.execute(sql, val)

    # Veritabanı işlemlerini tamamlama
    db.commit()
    
    print("Tarifler başarıyla veritabanına kaydedildi.")
except mysql.connector.Error as err:
    print(f"Hata: {err}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
