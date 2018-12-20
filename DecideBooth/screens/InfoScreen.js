import React from 'react';
import { StyleSheet } from 'react-native';
import { Container, Header, Content, Form, Item, Input, Button, Text } from 'native-base';

export default class InfoScreen extends React.Component {
  static navigationOptions = {
    title: 'Acerca de',
  };

  render() {
    return (

            <Content>
            <Text>{`
Esto es una plataforma de voto electrónico seguro que cumple una serie de garantías básicas, como la anonimicidad y el secreto del voto.

Los desarrolladores del proyecto son los miembros del grupo Wadobo.

Esta aplicación ha sido desarrollada por Pablo Tabares García, César García Pascual y Alfredo Campos Durán.
`}</Text>


            </Content>
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
