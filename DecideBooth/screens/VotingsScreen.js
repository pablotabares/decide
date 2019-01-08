import React from 'react';
import {AsyncStorage, StyleSheet} from 'react-native';
import { Container, Header, Content, List, ListItem, Text, Body, Right, Icon, Left, Button} from 'native-base';
import moment from "moment";

class VoteRightItem extends React.Component{
    render(){
        switch(this.props.status) {
            case 0:
                return (
                    <Right style={{flex:1,flexGrow:1}}>
                        <Text note>
                            No Date
                        </Text>
                    </Right>
                );
            case 1:
                return(
                    <Right style={{flex:1,flexGrow:1}}>
                        <Text note>
                            {moment(this.props.item.start_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ').format('DD/MM/YY')}
                        </Text>
                    </Right>
                );
            case 2:
                return(
                    <Right style={{flex:1,flexGrow:1}}>
                        <Text note>
                            Closed
                        </Text>
                    </Right>
                );
            default:
                return(
                    <Right style={{flex: 1, flexDirection: 'row',justifyContent: 'flex-end', flexGrow:1}}>
                        <Button onPress={() => this.props.onPress()} transparent primary>
                            <Text>Vote</Text>
                            <Icon name="arrow-forward" style={{marginLeft: 5, color: 'blue'}}/>
                        </Button>
                    </Right>
                );
        }
    }
}

class VoteItem extends React.Component{

    render(){
        let status = null;
        let icon = 'done';
        let icolor = 'green';
        if(this.props.item.start_date === null){
            status = 0;
            icon = 'stop';
            icolor = 'grey';
        }else if(moment() < moment(this.props.item.start_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')){
            status = 1;
            icon = 'timer';
            icolor = 'blue';
        }else if(moment() > moment(this.props.item.end_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ')){
            status = 2;
            icon = 'clear';
            icolor = 'red';
        }
        return(
            <ListItem noIndent style={{
                flex: 1,
                flexDirection: 'row',
            }}>
                <Left style={{flex:0,flexShrink:1}}>
                    <Icon name={icon} type='MaterialIcons' style={{color: icolor}}/>
                </Left>
                <Body style={{flex:0,flexGrow:1}}>
                <Text numberOfLines={1}>{this.props.item.name}</Text>
                <Text note numberOfLines={1}>{this.props.item.desc}</Text>
                </Body>
                <VoteRightItem style={{flex:0,flexGrow:1}} status={status} item={this.props.item} onPress={() => this.props.onPress()}/>
            </ListItem>
        )
    }
}


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
            fetch('http://decide-testing.herokuapp.com/census/voter/'+id, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if(response.status === 200) {
                        let votings = JSON.parse(response._bodyText);
                        this.setState({
                            votings: votings
                        });
                    }else{
                        console.error(response);
                    }
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
                          <VoteItem item={item} onPress={() => this._goVote(item.id)} />
                      }>
                </List>
            </Content>
        </Container>
    );
  }
}
