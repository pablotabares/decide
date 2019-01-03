import React from 'react';
import {AsyncStorage, StyleSheet} from 'react-native';
import { Container, Header, Content, List, ListItem, Text, Body, Right, Icon} from 'native-base';
import moment from "moment";

export default class VotingsScreen extends React.Component {
  static navigationOptions = {
    header: null,
  };

    constructor(props) {
        super(props);
        this.state = {
            votings : []
        }
    }

    _signOutAsync = async () => {
        await AsyncStorage.clear();
        this.props.navigation.navigate('Auth');
    };

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

    _goVote(voting_id) {
        this.props.navigation.push('Vote',{
            voting_id : voting_id.toString()
        });
    };

    componentWillMount() {
        this._getVotings();
    }

  render() {
    return (
        <Container>
            <Header/>
            <Content>
                <List dataArray={this.state.votings}
                      renderRow={(item) =>
                          <ListItem>
                              <Body>
                                  <Text>{item.name}</Text>
                                  <Text note>{item.desc}</Text>
                              </Body>
                                  {
                                      item.start_date === null || moment() < moment(item.start_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')
                                          ?
                                          <Right>
                                            <Text note>{
                                                item.start_date === null ?
                                                    'No Date'
                                                    :
                                                moment(item.start_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ').format('DD/MM/YY')
                                            }</Text>
                                          </Right>
                                              :
                                          (
                                              item.end_date === null || moment() < moment(item.end_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')
                                                  ?
                                                  <Right style={{flex: 1, flexDirection: 'row',justifyContent: 'flex-end'}}>
                                                    <Text>Vote</Text>
                                                    <Icon name="arrow-forward" style={{marginLeft: 5, color: 'blue'}}
                                                          onPress={() => this._goVote(item.id)}/>
                                                  </Right>
                                                      :
                                                  <Right>
                                                      <Icon name="close" type="MaterialIcons"/>
                                                  </Right>
                                          )
                                  }
                          </ListItem>
                      }>
                </List>
            </Content>
        </Container>
    );
  }
}
