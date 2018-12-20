import React from 'react';
import { StyleSheet } from 'react-native';
import { Container, Header, Content, Form, Item, Input, Button, Text } from 'native-base';

export default class ProfileScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    _signOutAsync = async () => {
        await AsyncStorage.clear();
        this.props.navigation.navigate('Auth');
    };

    render() {
        return (
            <Container>
                <Header/>
                <Content>
                    <Button full danger onPress={this._signOutAsync}>
                        <Text>Logout</Text>
                    </Button>
                </Content>
            </Container>
        );
    }
}
