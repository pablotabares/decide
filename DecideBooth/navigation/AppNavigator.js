import React from 'react';
import { Platform } from 'react-native';
import { createSwitchNavigator, createStackNavigator, createBottomTabNavigator, createNavigationContainer} from 'react-navigation';

import LoginScreen from '../screens/LoginScreen';
import AuthLoadingScreen from '../screens/AuthLoadingScreen';
import MainTabNavigator from '../navigation/MainTabNavigator';

const AuthStack = createStackNavigator({ Login: LoginScreen });

export default createNavigationContainer(createSwitchNavigator(
    {
      AuthLoading: AuthLoadingScreen,
      App: MainTabNavigator,
      Auth: AuthStack,
    },
    {
      initialRouteName: 'AuthLoading',
    }
));