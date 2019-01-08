import React from 'react';
import {
    Text,
    Alert,
    AsyncStorage
} from 'react-native';
import {Button, Container, Content, Form, Header, Input, Item} from "native-base";

export default class LoginScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        }
    }

    _submitLogin() {
        fetch('http://decide-testing.herokuapp.com/authentication/login/',{
            method: 'POST',
            headers: {
                'Accept' : 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password
            })
        })
            .then(response => {
                if(response.status === 400){
                    let errors = JSON.parse(response._bodyText).non_field_errors
                    if(typeof errors !== 'undefined'){
                        Alert.alert(
                            'Error',
                            errors[0],
                            [
                                {text: 'OK'},
                            ],
                            {cancelable: false}
                        )
                    }
                }else{
                    let userToken = JSON.parse(response._bodyText).token;
                    AsyncStorage.setItem('userToken', userToken);
                    fetch('http://decide-testing.herokuapp.com/authentication/getuser/',{
                        method: 'POST',
                        headers: {
                            'Accept' : 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            token: userToken
                        })
                    })
                    .then(response => {
                            AsyncStorage.setItem('userId', JSON.parse(response._bodyText).id.toString());
                            this.props.navigation.navigate('App');
                    })
                    .catch(error => console.error(error));
                }
            })
            .catch(error => console.error(error));
    }


    render() {
        return (
            <Container>
                <Header/>
                <Content>
                    <Form>
                        <Item>
                            <Input placeholder="Nombre de usuario" onChangeText={(text) => this.setState({username: text})}/>
                        </Item>
                        <Item last>
                            <Input placeholder="Contraseña" onChangeText={(text) => this.setState({password: text})}/>
                        </Item>
                        <Button full success onPress={this._submitLogin.bind(this)}>
                            <Text>Logon</Text>
                        </Button>
                    </Form>
                </Content>
            </Container>
        );
    }
}
