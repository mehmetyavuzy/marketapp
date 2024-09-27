import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../src/HomeScreen';
import SearchResultsScreen from '../src/SearchResultsScreen';

const Stack = createStackNavigator();  

const AppNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Home">
      <Stack.Screen name="Home" component={HomeScreen} options={{headerShown: false }} />
      <Stack.Screen name="SearchResults" component={SearchResultsScreen} options={{title:'Ürünler' }} />
    </Stack.Navigator>
  );
};

export default AppNavigator;
