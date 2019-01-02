import React from 'react';
import {AsyncStorage, StyleSheet} from 'react-native';
import { Container, Header, Content, List, ListItem, Text, Left, Right, Button, Radio, Body, Title, Subtitle, Icon, Card, CardItem} from 'native-base';

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
                                    this.setState({
                                        title : voting.name,
                                        desc : voting.desc,
                                        question_title : voting.question.desc,
                                        options: voting.question.options,
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
                    <Button full success>
                        <Text>Save</Text>
                    </Button>
                </Content>
            </Container>
        );
    }
}
