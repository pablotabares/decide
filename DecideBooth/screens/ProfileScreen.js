import React from 'react';
import {ScrollView, AsyncStorage, Text} from 'react-native';
import{
    Container,
    Header,
    Content,
    Button
} from "native-base";

export default class ProfileScreen extends React.Component {
  static navigationOptions = {
    header: null,
  };

  _signOutAsync = async () => {
    await AsyncStorage.clear();
    this.props.navigation.navigate('Auth');
  };

  render() {
    /* Go ahead and delete ExpoConfigView and replace it with your
     * content, we just wanted to give you a quick view of your config */
    return (
        <Container>
          <Header/>
          <Content>
            <ScrollView>
              <Button full danger onPress={this._signOutAsync}>
                <Text>Logout</Text>
              </Button>
            </ScrollView>
          </Content>
        </Container>
    )
  }
}
