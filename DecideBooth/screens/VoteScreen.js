import React from 'react';
import {AsyncStorage, StyleSheet} from 'react-native';
import { Container, Header, Content, List, ListItem, Text, Left, Right, Button, Radio, Body, Title, Subtitle, Icon, Card, CardItem} from 'native-base';
import BigInt from '../js/bigint';
import ElGamal from '../js/elgamal';

export default class VoteScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            title : '',
            desc : '',
            question_title : '',
            options : [],
            bigpk : null,
            itemSelected : null
        }
    }

    _signOutAsync = async () => {
        await AsyncStorage.clear();
        this.props.navigation.navigate('Auth');
    };

    _getBooth = async() => {
        const token = await AsyncStorage.getItem('userToken');
        const id = await AsyncStorage.getItem('userId');
        const voting_id = this.props.navigation.getParam('voting_id', '0');
        if(id !== null && token !== null) {
            if(voting_id !== '0') {
                fetch('http://decide-ortosia.herokuapp.com/census/' + voting_id + '/?voter_id=' + id, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                        if (response.status === 200) {
                            fetch('http://decide-ortosia.herokuapp.com/voting/?id=' + voting_id, {
                                method: 'GET',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                }
                            })
                                .then(response => {
                                    let voting = JSON.parse(response._bodyText)[0];
                                    let bigpk = {
                                        p: BigInt.fromJSONObject(voting.pub_key.p.toString()),
                                        g: BigInt.fromJSONObject(voting.pub_key.g.toString()),
                                        y: BigInt.fromJSONObject(voting.pub_key.y.toString()),
                                    };
                                    this.setState({
                                        title : voting.name,
                                        desc : voting.desc,
                                        question_title : voting.question.desc,
                                        options: voting.question.options,
                                        bigpk : bigpk
                                    })
                                })
                                .catch(error => console.error(error));
                        }
                    })
                    .catch(error => console.error(error));
            }else{
                this.props.navigation.goBack();
            }
        }else{
            this._signOutAsync();
        }
    };
    //   ElGamal.BITS = 256; //TODO: CHANGE FOR FETCH WITCH RETRIEVES KEYBITS FROM SETTINGS

    _decideEncrypt() {
        let msg = this.state.itemSelected;
        let bigmsg = BigInt.fromJSONObject(msg);
        let cipher = ElGamal.encrypt(this.state.bigpk, bigmsg);
        return cipher;
    };

    _decideSend = async() => {
        const token = await AsyncStorage.getItem('userToken');
        const id = await AsyncStorage.getItem('userId');
        const voting_id = this.props.navigation.getParam('voting_id', '0');
        var v = this._decideEncrypt();
        var data = {
            vote: {a: v.alpha.toString(), b: v.beta.toString()},
            voting: parseInt(voting_id),
            voter: parseInt(id),
            token: token
        };
        console.log(data);
        fetch("http://decide-ortosia.herokuapp.com/store/", {
            method : 'POST',
            headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if(response.status === 200) {
                    alert("Conglatulations. Your vote has been sent");
                    this.props.navigation.goBack();
                }else if(response.status === 401) {
                    alert("Error! Voting is not permitted");
                    this.props.navigation.goBack();
                }
            })
            .catch(error => {
                alert("Error: " + error);
                console.error(error);
            });
    };

    componentWillMount() {
        this._getBooth();
    }

    render() {
        return (
            <Container>
                <Header>
                    <Left>
                        <Button transparent onPress={() => this.props.navigation.goBack()}>
                            <Icon name="arrow-back" />
                        </Button>
                    </Left>
                    <Body>
                        <Title>{this.state.title}</Title>
                        <Subtitle>{this.state.desc}</Subtitle>
                    </Body>
                    <Right/>
                </Header>
                <Content padder>
                    <CardItem header bordered>
                        <Text>{this.state.question_title}</Text>
                    </CardItem>
                    <Card dataArray={this.state.options}
                          renderRow={(item) =>
                              <CardItem>
                                  <Left>
                                      <Text>{item.option}</Text>
                                  </Left>
                                  <Right>
                                      <Radio onPress={() => this.setState({ itemSelected: item.number })}
                                             selected={this.state.itemSelected === item.number}/>
                                  </Right>
                              </CardItem>
                          }>
                    </Card>
                    <Button full success onPress={this._decideSend.bind(this)}>
                        <Text>Save</Text>
                    </Button>
                </Content>
            </Container>
        );
    }
}
