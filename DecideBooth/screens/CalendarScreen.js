import React, {Component} from 'react';
import {
  Text,
  StyleSheet,
  ScrollView,
  View,
  Button
} from 'react-native';
import {Calendar} from 'react-native-calendars';

export default class CalendarsScreen extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.onDayPress = this.onDayPress.bind(this);
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Here you can set important voting dates</Text>
        <Calendar
          onDayPress={this.onDayPress}
          style={styles.calendar}
          hideExtraDays
          markedDates={{[this.state.selected]: {selected: true, disableTouchEvent: true, selectedDotColor: 'orange'}}}
        />  
			
      </View>
	  
	  
    );
  }

  onDayPress(day) {
    this.setState({
      selected: day.dateString
    });
  }
}

_getDates = async() => {
		const token = await AsyncStorage.getItem('userToken');
        const id = await AsyncStorage.getItem('userId');
		const endDate = await AsyncStorage.getItem('end_date');
		
        if(id !== null && token !== null && endDate !== null) {
			fetch('http://decide-ortosia.herokuapp.com/census/voter/'+id, {
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

const styles = StyleSheet.create({
  calendar: {
    borderTopWidth: 1,
    paddingTop: 5,
    borderBottomWidth: 1,
    borderColor: '#eee',
    height: 350
  },
  text: {
    textAlign: 'center',
    borderColor: '#bbb',
    padding: 10,
    backgroundColor: '#eee'
  },
  container: {
    flex: 1,
    backgroundColor: 'gray'
  }
});