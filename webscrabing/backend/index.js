const express = require('express');
const cors = require('cors');
const mysql = require('mysql');
const app = express();

app.use(cors());
app.use(express.json());

// MySQL bağlantısı
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'Mehmet69436943',  // MySQL şifrenizi buraya girin
  database: 'market_data'
});

db.connect((err) => {
  if (err) {
    console.error('Veritabanına bağlanırken bir hata oluştu:', err);
    return;
  }
  console.log('Veritabanına başarıyla bağlandı.');
});

// Arama endpoint'i
app.get('/search', (req, res) => {
  const productName = req.query.product_name;
  if (!productName) {
    return res.status(400).send('Product name is required');
  }

  const query = `
    SELECT 'Migros' AS market, product_name, price, image FROM migros_products WHERE product_name LIKE ?
    UNION
    SELECT 'Bizim' AS market, product_name, price, image FROM bizim_products WHERE product_name LIKE ?
    UNION
    SELECT 'Şok' AS market, product_name, price, image FROM sok_products WHERE product_name LIKE ?
  `;

  db.query(query, [`%${productName}%`, `%${productName}%`, `%${productName}%`], (err, results) => {
    if (err) {
      console.error('Veritabanı sorgusunda bir hata oluştu:', err);
      return res.status(500).send('Server error');
    }

    // Veritabanındaki LONGBLOB tipindeki veriyi base64'e çevir
    results.forEach((item) => {
      if (item.image) {
        item.image = Buffer.from(item.image).toString('base64');
      }
    });

    res.json(results);
  });
});

app.listen(3000, () => {
  console.log('Sunucu http://localhost:3000 adresinde çalışıyor.');
});
