import React from 'react';
import { StyleSheet, TextInput, View, Button } from 'react-native';
import axios from 'axios';

import PlayerScore from './components/PlayerScore';
import PlayerNameInput from './components/PlayerNameInput';

export default class App extends React.Component {
	getPointsInterval = 0;

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

		this.adjustScore = this.adjustScore.bind(this);
	}
	
	getPoints = () => {
		let data = {
			'activePlayer': this.state.activePlayer
		}		
		console.log('calling get points')
		axios.get('https://ukce.danjscott.co.uk/api/game/player_points/' + this.state.gameId)
			.then((res) => {
				console.log(res.data);
				// let dbPlayerOnePoints = res.data['player_one_points']; 
				// let dbPlayerTwoPoints = res.data['player_two_points']; 
				this.setState({
					playerOnePoints: res.data['player_one_points'],
					playerTwoPoints: res.data['player_two_points']
				});
				// const points = res.data.points;
				// console.log('points: ' + points)
				// switch(this.state.activePlayer){
				// 	case 'player_one':
				// 		this.setState({playerOnePoints: points});
				// 		break;
				// 	case 'player_two':
				// 		this.setState({playerTwoPoints: points});
				// 		break;
				// 	default:
				// 		break;
				// }
			});
	}

	changePlayer = () => {
		switch(this.state.activePlayer){
			case 'player_one':
				this.setState({activePlayer: 'player_two'});
				break;
			case 'player_two':
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
		// alert(this.state.websocketServerIp);
		let connection = new WebSocket('ws://' + this.state.websocketServerIp + ':8765');
		let msg = 'start#' + this.state.gameId;
		connection.onopen = () => {
			connection.send(msg);
			this.getPointsInterval = setInterval(this.getPoints, 4000);
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
		});
		clearInterval(this.getPointsInterval);
	}

	async adjustScore(activePlayer, increment){
		var data = {
			'activePlayer': activePlayer,
			'increment': increment
		}

		res = await axios.post('https://ukce.danjscott.co.uk/api/game/manual_points/'  + this.state.gameId, data)
		if(res.status === 200){
			switch(activePlayer){
				case 'player_one':
					if(increment){
						this.setState({
							playerOnePoints: this.state.playerOnePoints + 1
						});
					}
					else{
						if(this.state.playerOnePoints > 0){
							this.setState({
								playerOnePoints: this.state.playerOnePoints - 1
							});
						}
					}
					break;
				case 'player_two':
					if(increment){
						this.setState({
							playerTwoPoints: this.state.playerTwoPoints + 1
						});
					}
					else{
						if(this.state.playerTwoPoints > 0){
							this.setState({
								playerTwoPoints: this.state.playerTwoPoints - 1
							});
						}
					}
					break;
				default:
					break;
			}
		}
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
							<View style={styles.btnContainerTwo}>
								<View style={styles.btnManualScores}>
									<Button
									onPress={() => this.adjustScore('player_one', true)}
									title="+"
									color="#f5c537"
									/>
								</View>
								<View style={styles.btnManualScores}>
									<Button
										onPress={() => this.adjustScore('player_one', false)}
										title="-"
										color="#f5c537"
									/>
								</View>
							</View>
							<View style={{marginTop: 25, marginBottom: 25}}></View>
							<PlayerScore name={this.state.playerTwoName} active={this.state.playerTwoActive} score={this.state.playerTwoPoints} />
							<View style={styles.btnContainerTwo}>
								<View style={styles.btnManualScores}>
									<Button
									onPress={() => this.adjustScore('player_two', true)}
									title="+"
									color="#f5c537"
									/>
								</View>
								<View style={styles.btnManualScores}>
									<Button
										onPress={() => this.adjustScore('player_two', false)}
										title="-"
										color="#f5c537"
									/>
								</View>
							</View>
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
		// marginTop: 5
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
	btnContainerTwo: {
		// paddingTop: 25,
		// paddingBottom: 25,
		flexWrap: 'wrap', 
        alignItems: 'flex-start',
		flexDirection: 'row',
		// justifyContent: 'space-between',
	},
	btn: {
		margin: 10,
		width: '40%'
	},
	btnManualScores: {
		margin: 10,
		marginLeft: 50,
		width: '30%'
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
