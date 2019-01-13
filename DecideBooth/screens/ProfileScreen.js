import React from 'react';
import {Alert, AsyncStorage} from 'react-native';
import { Container, Header, Content, Button, Text, Card, CardItem, Icon, Spinner, Right } from 'native-base';

export default class ProfileScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            is_staff: '',
            loaded: false,
        }
    }

    _signOutAsync = async () => {
        await AsyncStorage.clear();
        this.props.navigation.navigate('Auth');
    };

    _getProfileInfo = async() => {
        const token = await AsyncStorage.getItem('userToken');
        if(token !== null) {
            fetch('http://decide-ortosia.herokuapp.com/authentication/getuser/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token
                })
            })
                .then(response => {
                    let user = JSON.parse(response._bodyText);
                    this.setState({
                        username: user.username,
                        first_name: user.first_name,
                        last_name: user.last_name,
                        email: user.email,
                        is_staff: user.is_staff,
                        loaded: true
                    });
                })
                .catch(error => console.error(error));
        }else{
            this._signOutAsync();
        }
    };

    componentWillMount() {
        this._getProfileInfo();
    }

    render() {
        return (
            <Container>
                <Header/>
                <Content>
                    <Card>
                        <CardItem header bordered>
                            <Text>My Profile</Text>
                        </CardItem>
                        <CardItem>
                            <Icon active name="person" type="MaterialIcons" />
                            <Text>{this.state.first_name} {this.state.last_name}</Text>
                        </CardItem>
                        <CardItem>
                            <Icon active name="keyboard" type="MaterialIcons" />
                            <Text>{this.state.username}</Text>
                        </CardItem>
                        <CardItem>
                            <Icon active name="email" type="MaterialIcons" />
                            <Text>{this.state.email}</Text>
                        </CardItem>
                        {
                            this.state.is_staff ?
                                <CardItem>
                                    <Icon active name="star" type="MaterialIcons" style={{color: 'yellow'}}/>
                                    <Text style={{fontWeight: 'bold'}}>Staff Member</Text>
                                </CardItem>
                                :
                                null
                        }
                    </Card>
                    <Button full danger onPress={this._signOutAsync}>
                        <Text>Logout</Text>
                    </Button>
                    <Spinner animating={!this.state.loaded} color='blue' size='large'/>
                </Content>
            </Container>
        );
    }
}
