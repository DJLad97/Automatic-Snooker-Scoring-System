import React, { Component } from 'react';
import axios from 'axios';
import { Button, Container, Row, Col } from 'reactstrap';
import PlayerScore from './components/PlayerScore';
import PlayerNameInput from './components/PlayerNameInput';
import './App.css';

class App extends Component {

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

	async adjustScore(activePlayer, increment){
		var data = {
			'activePlayer': activePlayer,
			'increment': increment
		}

		var res = await axios.post('https://ukce.danjscott.co.uk/api/game/manual_points/'  + this.state.gameId, data)
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
		const players = this.state.players || [];
		return (
			<div className="App">
				<Container className="main">
				{
					!this.state.showScores && (
						<PlayerNameInput showNextComponent={this.showNextComponent}></PlayerNameInput>
						)
					}
				{
					(this.state.showScores) && (
						<div>
							<PlayerScore name={this.state.playerOneName} active={this.state.playerOneActive} score={this.state.playerOnePoints}/>
							<Row>
								<Col xs={{span:4, offset: 2}}>
									<Button
									onClick={() => this.adjustScore('player_one', true)}
									color="warning"
									className="inc-btn"
									>+</Button>
									<Button
										onClick={() => this.adjustScore('player_one', false)}
										color="warning"
										className="dec-btn"
									>-</Button>
								</Col>
							</Row>
							<PlayerScore name={this.state.playerTwoName} active={this.state.playerTwoActive} score={this.state.playerTwoPoints}/>
							<Row>
								<Col xs={{span:4, offset: 2}}>
									<Button
									onClick={() => this.adjustScore('player_two', true)}
									color="warning"
									className="inc-btn"
									>+</Button>
									<Button
										onClick={() => this.adjustScore('player_two', false)}
										color="warning"
										className="dec-btn"
									>-</Button>
								</Col>
							</Row>
							<Row>
								<Col xs={2} sm={2}></Col>
								<Col xs={{span:4}} sm={{span:4}}>
									<Button color="success" onClick={this.start}>Start</Button>
								</Col>
								<Col xs={2} sm={2}></Col>
								<Col xs={{span:4}} sm={{span:4}}>
									<Button color="primary" onClick={this.changePlayer}>Change Player</Button>
								</Col>
							</Row>
							<br/>
							<Row>
								<Col xs={{size:4, offset: 4}} sm={{size:4, offset: 4}}>
									<Button color="danger" onClick={this.endGame}>End Game</Button>
								</Col>
							</Row>

						</div>
					)
				}
				</Container>
			</div>
		);
	}
}

export default App;
