import React from 'react';
import { StyleSheet, TextInput, View, Button } from 'react-native';
import axios from 'axios';

import PlayerScore from './components/PlayerScore';
import PlayerNameInput from './components/PlayerNameInput';

export default class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			players: [],
			playerOneName: '',
			playerOnePoints: 0,
			playerTwoName: '',
			playerTwoPoints: 0,
			activePlayer: '',
			gameId: 0,
			showScores: false,
			playerOneActive: true,
			playerTwoActive: false,
			websocketServerIp: ''
		}
	}
	
	getPoints = () => {
		let data = {
			'activePlayer': this.state.activePlayer
		}		
		axios.get('https://ukce.danjscott.co.uk/api/game/player_points/' + this.state.gameId, {params: {'activePlayer': this.state.activePlayer}})
			.then((res) => {
				const points = res.data.points;
				switch(this.state.activePlayer){
					case 'player_one':
						this.setState({playerOnePoints: points});
						break;
					case 'player_two':
						this.setState({playerTwoPoints: points});
						break;
					default:
						break;
				}
				console.log('active player: ' + this.state.activePlayer)
			});
		
	
		// axios.get('https://ukce.danjscott.co.uk/api/player/' + this.state.player[1].id)
		// 	.then((res) => {
		// 		this.setState({playerTwoPoints: res.data.points});
		// 	});
	}

	changePlayer = () => {
		switch(this.state.activePlayer){
			case 'player_one':
				this.setState({activePlayer: 'player_two'});
				break;
			case this.state.playerTwoName:
				this.setState({activePlayer: 'player_one'});
				break;
			default:
				break;
		}
		this.setState({
			playerOneActive: !this.state.playerOneActive, 
			playerTwoActive: !this.state.playerTwoActive
		});

		axios.post('https://ukce.danjscott.co.uk/api/game/active_player/' + this.state.gameId)
	}

	showNextComponent = (playerOne, playerTwo) => {
		// this.setState({showScores: true})
		// alert('playerOne: ' + playerOne);
        // alert('playerTwo: ' + playerTwo);
		var config = {
			headers: {'Access-Control-Allow-Origin': '*'}
		};

		axios.get('https://ukce.danjscott.co.uk/api/game')
			.then((res) => {
				console.log(res.data.id);
				console.log(res.data.vision_system_ip);
				this.setState({
					playerOneName: playerOne, 
					playerTwoName: playerTwo,
					activePlayer: 'player_one',
					gameId: res.data.id,
					showScores: true,
					websocketServerIp: res.data.vision_system_ip
				});
			});

	}

	start = () => {
		let connection = new WebSocket('ws://' + this.state.websocketServerIp + ':8765');
		let msg = 'start#' + this.state.gameId;
		// alert(msg);
		connection.onopen = () => {
			// connection.send('start');
			// alert(msg)
			connection.send(msg);
			setInterval(this.getPoints, 3500);

		}
	}

	endGame = () => {
		this.setState({
			players: [],
			playerOneName: '',
			playerOnePoints: 0,
			playerTwoName: '',
			playerTwoPoints: 0,
			activePlayer: '',
			gameId: 0,
			showScores: false,
			playerOneActive: true,
			playerTwoActive: false,
			websocketServerIp: ''
		})
	}

	render() {
		return (
			<View style={styles.container}>
				{
					(!this.state.showScores) && (
						<View>
							<PlayerNameInput showNextComponent={this.showNextComponent}/>
						</View>
					)
				}
				{
					(this.state.showScores) && (
						<View>
							<PlayerScore name={this.state.playerOneName} active={this.state.playerOneActive} score={this.state.playerOnePoints} />
							<View style={{marginTop: 25, marginBottom: 25}}></View>
							<PlayerScore name={this.state.playerTwoName} active={this.state.playerTwoActive} score={this.state.playerTwoPoints} />

							<View style={styles.btnContainer}>
								<View style={styles.btn}>
									<Button
									onPress={this.start}
									title="Start"
									color="#217940"
									/>
								</View>
								<View style={styles.btn}>
									<Button
										onPress={this.changePlayer}
										style={styles.btn}
										title="Change Player"
										color="#217940"
									/>
								</View>
								<View style={styles.endBtn}>
									<Button
										onPress={this.endGame}
										style={styles.btn}
										title="End Game"
										color="#c73434"
									/>
								</View>
							</View>
						</View>
					)
				}
			</View>
		);
	}
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: '#282c34',
		alignItems: 'center',
		justifyContent: 'center',
	},
	scoreBlock: {
		alignItems: 'center',
		marginTop: 5
	},
	playerName: {
		// font-size: calc(100px + 2vmin);
		color: '#fff',
		fontSize: 78,
		// marginTop: 80
	},
	
	playerPoints: {
		color: '#fff',
		fontSize: 108,
		// marginTop: 50
	},
	btnContainer: {
		// paddingTop: 25,
		// paddingBottom: 25,
		flexWrap: 'wrap', 
        alignItems: 'flex-start',
		flexDirection: 'row',
		justifyContent: 'space-between',
		paddingTop: 50
	},
	btn: {
		margin: 10,
		width: '40%'
	},
	endBtn: {
		// margin: auto
		// flex: 1,
		marginLeft: 10,
		marginRight: 10,
		marginTop: 25,
		width: '95%',
		// alignItems: 'flex-start'
	}
});
