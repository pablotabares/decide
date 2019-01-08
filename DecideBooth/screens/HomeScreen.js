import React from 'react';
import {
  Image,AsyncStorage, StyleSheet, Alert,Modal, TouchableHighlight, View,
} from 'react-native';
import {Container, Header, Content, Button,Card, CardItem, Icon, List, ListItem, Accordion,Body, Title,Text, Left, Right } from "native-base";
import {NavigationActions} from "react-navigation";
import moment from "moment";

const dataArray = [
{ title: "My votings", content:"AAA" },
{ title: "Popular votings", content: "Lorem ipsum dolor sit amet" }
];

///////////////////////////////////////////////////////////////////////////////
//////////////////////////////////SCREENS//////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
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

              <CardItem/>

              <CardItem header style={{flex: 1, flexDirection:'row',justifyContent: 'center', alignItems:'flex-start'}}>
                  <Text style={{fontWeight: 'bold', fontSize:25}}>Welcome to Decide</Text>
              </CardItem>

              <CardItem  bordered style={{flex: 1, flexDirection:'row',justifyContent: 'center', alignItems:'flex-start'}} >
                <Image
                  style={{height:75,flex: 1, flexDirection:'row',alignSelf:'stretch'}}
                  source={require('../img/banner.jpeg')}
                />
              </CardItem>

              <CardItem style={{flex: 1, flexDirection:'row',justifyContent: 'flex-start', alignItems:'flex-start'}}>
                  <Text style={{fontWeight: 'bold', fontSize:14}}>Completed votings</Text>
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


///////////////////////////////////////////////////////////////////////////////
//////////////////////////////////ITEMS//////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

class VoteItem extends React.Component{

  state = {
    modalVisible: false,
  };

  setModalVisible(visible, voting_id) {
    this.setState({modalVisible: visible});
  }

    render(){
        if(moment() > moment(this.props.item.end_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')){
          return(
            <View style={{marginTop: 22}}>
              <Modal
                animationType="slide"
                transparent={false}
                visible={this.state.modalVisible}
                onRequestClose={() => {
                  Alert.alert('Modal has been closed.');
                }}>
                <View style={{marginTop: 22}}>
                  <View>
                    <Text>Hello World!</Text>

                    <TouchableHighlight
                      onPress={() => {
                        this.setModalVisible(!this.state.modalVisible);
                      }}>
                      <Text>Hide Modal</Text>
                    </TouchableHighlight>
                  </View>
                </View>
              </Modal>
              <ListItem noIndent onPress={() => {this.setModalVisible(true, this.props.item.id);}}
                style={{
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
            </View>
          )
        } else {return null}
    }
}
