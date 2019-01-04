import React from 'react';
import {
  Text,
} from 'react-native';
import {Container, Content, Header} from "native-base";
import {NavigationActions} from "react-navigation";

export default class HomeScreen extends React.Component {
  static navigationOptions = {
    header: null,
  };

  constructor(props){
    super(props);
  }

  render() {
    // const {navigate} = this.props.navigation;
    // console.log(typeof this.token);
    // if(this.navigation.state.token === undefined) navigate('Login');
    return (
        <Container>
          <Header/>
          <Content>
            <Text>Home Screen: </Text>
          </Content>
        </Container>
    );
  }
}
