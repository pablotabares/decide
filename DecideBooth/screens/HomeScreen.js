import React from 'react';
import {
  Image,
} from 'react-native';
import {Container, Header, Content, Button,Card, CardItem, Icon, Accordion,Body, Title,Text, Left, Right } from "native-base";
import {NavigationActions} from "react-navigation";

const dataArray = [
{ title: "My votings", content:"AAA" },
{ title: "Popular votings", content: "Lorem ipsum dolor sit amet" }
];


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
          <Header>
            <Title>Home</Title>
          </Header>
          <Content>
            <Card >

                <CardItem>
                    <Text style={{fontWeight: 'bold'}}>Welcome to Decide</Text>
                </CardItem>

                <CardItem header bordered >
                  <Image
                    style={{width: 322,height: 60}}
                    source={require('../img/banner.jpeg')}
                  />
                </CardItem>

                <CardItem>
                    <Accordion dataArray={dataArray} />
                </CardItem>
            </Card>
          </Content>
        </Container>
    );
  }
}
