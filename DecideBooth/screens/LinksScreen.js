import React from 'react';
import { StyleSheet } from 'react-native';
import { Container, Header, Content, Form, Item, Input, Button, Text } from 'native-base';

export default class LinksScreen extends React.Component {
  static navigationOptions = {
    title: 'Links',
  };

  render() {
    return (
        <Container>
            <Header />
            <Content>
                <Form>
                    <Item>
                        <Input placeholder="Nombre de usuario" />
                    </Item>
                    <Item last>
                        <Input placeholder="Contraseña" />
                    </Item>
                  <Button full success>
                      <Text>Logon</Text>
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
