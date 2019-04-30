import React, { Component } from 'react';
import { StyleSheet, TextInput, View, Button } from 'react-native';

class PlayerNameInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            playerOneName: '',
            playerTwoName: ''
        }
    }

    submitNames = () => {
        let playerNames = {
            "player_names": [this.state.playerOneName, this.state.playerTwoName]
        }
        let playerOne = this.state.playerOneName;
        let playerTwo = this.state.playerTwoName;
        // alert('playerOne: ' + playerOne);
        // alert('playerTwo: ' + playerTwo);
        this.props.showNextComponent(playerOne, playerTwo);

    }
    
    render() {
        return (
            <View style={styles.nameIputContainer}>
                <TextInput
                style={styles.nameInput}
                placeholder="Player One Name"
                onChangeText={(text) => this.setState({playerOneName: text})}
                />
                <TextInput
                style={styles.nameInput}
                placeholder="Player Two Name"
                onChangeText={(text) => this.setState({playerTwoName: text})}
                />
                <View style={styles.submitBtn}>
                    <Button
                        onPress={this.submitNames}
                        title="Submit"
                        color="#217940"
                    />
                </View>
                {/* <Label for="playerOneName">Player One Name:</Label>
                <Input type="text" onChaange={this.onChange} name="playerOneName" placeholder="Name" />
                <Label for="playerTwoName">Player Two Name:</Label>
                <Input type="text" onChange={this.onChange} name="playerTwoName" placeholder="Name" />
                <Button color="primary" onClick={this.submitNames}>Submit</Button> */}
            </View>
        );
    }
}

export default PlayerNameInput;

const styles = StyleSheet.create({
	nameIputContainer: {
		// paddingTop: 25,
		// paddingBottom: 25,
		flexWrap: 'wrap', 
        alignItems: 'center',
		flexDirection: 'column',
		justifyContent: 'center',
    },
    nameInput: {
        width: '150%', 
        borderRadius: 5, 
        padding: 10, 
        margin: 25,
        backgroundColor: '#49505f', 
        color: '#fff'
    },
    submitBtn: {
		margin: 25,
		width: '150%'
	}
});
