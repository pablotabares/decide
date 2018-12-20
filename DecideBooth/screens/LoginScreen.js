import React from 'react';
import { StyleSheet, Alert } from 'react-native';
import { Container, Header, Content, Form, Item, Input, Button, Text } from 'native-base';

export default class LoginScreen extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            userName : '',
            password : '',
            token : '',
        }
    }
  static navigationOptions = {
    title: 'Login',
  };

  _onPressButton(){
      return fetch('https://decide-ortosia.herokuapp.com/authentication/login/', {
          method: 'POST',
          referrer: 'origin',
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              username: this.state.userName,
              password: this.state.password,
          }),
      })
      .then((response) => response.json())
      .then((responseJson) => {
          this.setState({token: responseJson.token});
      })
      .catch((error) => {
          console.error(error);
      })
  }

  render() {
    return (
        <Container>
            <Content>
                <Form>
                    <Item>
                        <Input onChangeText={(text) => this.setState({userName: text})} placeholder="Nombre de usuario" />
                    </Item>
                    <Item last>
                        <Input onChangeText={(text) => this.setState({password: text})} placeholder="Contraseña" />
                    </Item>
                  <Button full success onPress={this._onPressButton.bind(this)}>
                      <Text>Login</Text>
                  </Button>
                </Form>
            </Content>
        </Container>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 15,
    backgroundColor: '#fff',
  }
});
