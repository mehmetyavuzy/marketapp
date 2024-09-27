import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, Image } from 'react-native';
import axios from 'axios';

const SearchResultsScreen = ({ route, navigation }) => {
  const { query } = route.params;
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get(`http://10.0.2.2:3000/search?product_name=${query}`);
        console.log(response.data); // API'den gelen veriyi kontrol et
        setResults(response.data);
      } catch (error) {
        console.error('API çağrısı sırasında hata:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [query]);

  if (loading) {
    return <Text style={styles.loadingText}>Yükleniyor...</Text>;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={results}
        keyExtractor={(item, index) => {
          const uniqueKey = item.id ? item.id.toString() : `${item.product_name}-${item.market}-${index}`;
          return uniqueKey;
        }}
        renderItem={({ item }) => (
          <View style={styles.itemContainer}>
            {item.image ? (
              <Image source={{ uri: `data:image/jpeg;base64,${item.image}` }} style={styles.image} />
            ) : (
              <Text style={styles.noImage}>Resim mevcut değil</Text>
            )}
            <View style={styles.textContainer}>
              <Text style={styles.market}>{item.market}</Text>
              <Text style={styles.itemName}>{item.product_name}</Text>
              <Text style={styles.price}>{item.price} TL</Text>
            </View>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 10,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 3,
  },
  image: {
    width: 50,
    height: 50,
    marginRight: 16,
    borderRadius: 25,
  },
  noImage: {
    width: 50,
    height: 50,
    marginRight: 16,
    backgroundColor: '#ccc',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    lineHeight: 50,
    borderRadius: 25,
  },
  textContainer: {
    flex: 1,
  },
  market: {
    fontWeight: 'bold',
    color: '#333',
  },
  itemName: {
    fontSize: 16,
    color: '#555',
  },
  price: {
    color: 'green',
    fontWeight: 'bold',
  },
  loadingText: {
    textAlign: 'center',
    marginTop: 20,
    fontSize: 18,
    color: '#333',
  },
});

export default SearchResultsScreen;
