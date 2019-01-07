import React from 'react';
import {
  Image,AsyncStorage, StyleSheet, Alert
} from 'react-native';
import {Container, Header, Content, Button,Card, CardItem, Icon, List, ListItem, Accordion,Body, Title,Text, Left, Right } from "native-base";
import {NavigationActions} from "react-navigation";
import moment from "moment";

const dataArray = [
{ title: "My votings", content:"AAA" },
{ title: "Popular votings", content: "Lorem ipsum dolor sit amet" }
];


export default class HomeScreen extends React.Component {
  static navigationOptions = {
    header: null,
  };

  constructor(props) {
      super(props);
      this.state = {
          votings : []
      }
  }


  _getVotings = async() => {
      const token = await AsyncStorage.getItem('userToken');
      const id = await AsyncStorage.getItem('userId');
      if(id !== null && token !== null) {
          fetch('http://decide-ortosia.herokuapp.com/census/voter/'+id, {
              method: 'GET',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              }
          })
              .then(response => {
                  let votings = JSON.parse(response._bodyText);
                  this.setState({
                      votings: votings
                  });
              })
              .catch(error => console.error(error));
      }else{
          this._signOutAsync();
      }
  };




  componentWillMount() {
      this._getVotings();
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
                  <List dataArray={this.state.votings}
                        renderRow={(item) =>
                            <VoteItem item={item} />
                        }>
                  </List>
                </CardItem>
            </Card>
          </Content>
        </Container>
    );
  }
}


class VoteItem extends React.Component{

  _showVoting(voting_id) {
    Alert.alert('EEEEEE'+voting_id)
  }

    render(){
        if(moment() > moment(this.props.item.end_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')){
          return(
              <ListItem noIndent onPress={() =>this._showVoting(this.props.item.id)} style={{
                  flex: 1,
                  flexDirection: 'row',
                  justifyContent: 'space-between',
              }}>
                  <Left>
                      <Icon name='check' type='MaterialIcons' style={{color: 'green'}}/>
                  </Left>
                  <Body>
                  <Text>{this.props.item.name}</Text>
                  <Text note>{this.props.item.desc}</Text>
                  </Body>
              </ListItem>
          )
        } else {return null}
    }
}
