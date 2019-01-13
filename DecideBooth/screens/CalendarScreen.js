import React, {Component} from 'react';
import {
  Text,
  StyleSheet,
  ScrollView,
  View, AsyncStorage
} from 'react-native';
import {Body, Right, Button} from 'native-base';
import {Agenda} from 'react-native-calendars';
import moment from "moment";
import {VoteItem} from "../screens/VotingsScreen";

export default class CalendarsScreen extends Component {
  constructor(props) {
    super(props);
    this.state = {
      calendarItems : {}
    };
    this.onDayPress = this.onDayPress.bind(this);
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
            if(response.status === 200) {
              let votings = JSON.parse(response._bodyText);
              let calendarItems = {};
              votings.map((voting) => {
                if(voting.start_date !== null){
                  let sd = moment(voting.start_date,'YYYY-MM-DDTHH:mm:ss.SSSSSSZ').format('YYYY-MM-DD');
                  if(typeof calendarItems[sd] === 'undefined'){
                    calendarItems[sd] = [voting];
                  }else{
                    calendarItems[sd].push(voting);
                  }
                }
              });
              this.setState({calendarItems:calendarItems});
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

  renderItem(item) {
    return (
        <VoteItem item={item} onPress={() => this._goVote(item.id)} />
    );
  }

  rowHasChanged(r1, r2) {
    return r1.name !== r2.name;
  }

  timeToString(time) {
    const date = new Date(time);
    return date.toISOString().split('T')[0];
  }

    componentWillMount() {
    this._getVotings();
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Here you can see important voting dates</Text>
        <Agenda
          onDayPress={this.onDayPress}
          style={styles.calendar}
          // hideExtraDays
          items={this.state.calendarItems}
          // markingType={'multi-dot'}
          renderEmptyDate={() => {return (<View />);}}
          renderItem={this.renderItem.bind(this)}
          rowHasChanged={this.rowHasChanged.bind(this)}
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