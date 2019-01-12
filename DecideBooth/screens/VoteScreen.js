import React from 'react';
import {AsyncStorage} from 'react-native';
import { Container, Header, Content, List, Text, Left, Right, Button, Body, Title, Subtitle, Icon, Card, CardItem, ActionSheet} from 'native-base';
import BigInt from '../js/bigint';
import ElGamal from '../js/elgamal';
import ListItem from "react-native/local-cli/templates/HelloNavigation/components/ListItem";

export default class VoteScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            title: '',
            desc: '',
            questions: [],
            bigpk: null,
            itemsSelected: {}
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
                                    console.log(response);
                                    let voting = JSON.parse(response._bodyText)[0];
                                    let bigpk = {
                                        p: BigInt.fromJSONObject(voting.pub_key.p.toString()),
                                        g: BigInt.fromJSONObject(voting.pub_key.g.toString()),
                                        y: BigInt.fromJSONObject(voting.pub_key.y.toString()),
                                    };
                                    this.setState({
                                        title : voting.name,
                                        desc : voting.desc,
                                        questions: voting.questions,
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
        let msg = this.state.itemsSelected;
        let bigmsg = BigInt.fromJSONObject(JSON.stringify(msg));
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
                }else{
                    alert("Error");
                    console.log(response);
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
                    {/*<List dataArray={this.state.questions}*/}
                          {/*renderRow={(question) =>*/}
                          <List>
                              {this.state.questions.map((question,i) => {
                                  return (
                                      <Card key={question.desc} header bordered>
                                          <CardItem header>
                                              <Text>{question.desc}</Text>
                                          </CardItem>
                                          <Button full bordered onPress={() => {
                                                let buttons = Array.from(question.options, x => x.option + '    (' + x.number + ')');
                                                let len = buttons.push('Delete Selection');
                                                ActionSheet.show(
                                                    {
                                                        options: buttons,
                                                        destructiveButtonIndex: len - 1,
                                                        title: question.desc
                                                    },
                                                    buttonIndex => {
                                                        if(buttonIndex === len - 1){
                                                            let newSelection = this.state.itemsSelected;
                                                            delete newSelection[question.desc];
                                                            this.setState({itemsSelected: newSelection});
                                                        }else {
                                                            let newSelection = this.state.itemsSelected;
                                                            newSelection[question.desc] = /\(([0-9]+)\)/.exec(buttons[buttonIndex])[1];
                                                            this.setState({itemsSelected: newSelection});
                                                        }
                                                    }
                                                )
                                          }}>
                                              <Text>{typeof this.state.itemsSelected[question.desc] !== 'undefined'
                                                  ?
                                                  question.options.find((option) => {return this.state.itemsSelected[question.desc] === option.number.toString()}).option
                                                  :
                                                  '-- Select an option --'
                                              }</Text>
                                          </Button>
                                          {/*<Card transparent dataArray={question.options}*/}
                                                {/*renderRow={(option) =>*/}
                                                    {/*<CardItem>*/}
                                                        {/*<Left>*/}
                                                            {/*<Text>{option.option}</Text>*/}
                                                        {/*</Left>*/}
                                                        {/*<Right>*/}
                                                            {/*<Radio onPress={() => {*/}
                                                                {/*console.log('---------------------------');*/}
                                                                {/*console.log('q: '+question.desc);*/}
                                                                {/*console.log('option: '+option.number);*/}
                                                                {/*console.log(this.state.itemsSelected);*/}
                                                                {/*console.log(this.state.itemsSelected[question.desc] === option.number);*/}
                                                                {/*let itemsSelected = this.state.itemsSelected;*/}
                                                                {/*itemsSelected[question.desc] = option.number;*/}
                                                                {/*this.setState({itemsSelected: itemsSelected});*/}
                                                                {/*console.log(this.state.itemsSelected);*/}
                                                                {/*console.log(this.state.itemsSelected[question.desc] === option.number);*/}
                                                            {/*}}*/}
                                                                   {/*selected={this.state.itemsSelected[question.desc] === option.number}/>*/}
                                                        {/*</Right>*/}
                                                    {/*</CardItem>*/}
                                                {/*}>*/}
                                          {/*</Card>*/}
                                      </Card>
                                  )})}
                    </List>
                    <Button full success onPress={this._decideSend.bind(this)}>
                        <Text>Save</Text>
                    </Button>
                </Content>
            </Container>
        );
    }
}
