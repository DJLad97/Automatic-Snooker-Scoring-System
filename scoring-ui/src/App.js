import React, { Component } from 'react';
import axios from 'axios';
import { Button, Container, Row, Col } from 'reactstrap';
// import Websocket from 'react-websocket';
// import Websocket from 'websocket';
// import openSocket from 'socket.io-client';
import DigitRoll from 'digit-roll-react';
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
			showScores: false
			// socket: openSocket('ws://localhost:8765')
		}
		
	}
	componentDidMount(){
		// let connection = new WebSocket('ws://localhost:8765');
		// connection.onopen = () => {
		// 	connection.send('start');
		// 	// connection.send('change player');
			
		// }

		// this.setPlayerNames();
		// console.log(this.state.players);
		// this.readDatabase();
		// this.getPoints();
		
	}
	
	getPoints = () => {
		console.log('calling get points')
		let data = {
			'activePlayer': this.state.activePlayer
		}		
		axios.get('https://ukce.danjscott.co.uk/api/game/' + this.state.gameId, {params: {'activePlayer': this.state.activePlayer}})
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

	setPlayerNames = () => {
		let playerOne = 'Dan';
		let playerTwo = 'Ronnie';

		axios.get('https://ukce.danjscott.co.uk/api/players/')
			.then((res) => {
				console.log(res);
				const players = res.data;
				let tempPlayers = [];
				players.forEach((player, index) => {
					const playerObj = {
						'id': player.id,
						'name': player.name,
						'points': player.points
					}
					tempPlayers.push(playerObj);
					// console.log(player);
				})
				tempPlayers = tempPlayers.reverse();
				console.log(tempPlayers);
				this.setState({players: tempPlayers, showScores: true});
				setInterval(this.getPoints, 3500);
			});


		// axios.get('https://ukce.danjscott.co.uk/api/player/' + playerOne)
		// 	.then((res) => {
		// 		this.setState({playerOneName: res.data.name});
		// 		this.setState({playerOnePoints: res.data.points});
		// 	});

		// axios.get('https://ukce.danjscott.co.uk/api/player/' + playerTwo)
		// 	.then((res) => {
		// 		this.setState({playerTwoName: res.data.name});
		// 		this.setState({playerTwoPoints: res.data.points});
		// 	});
	}

	showNextComponent = (playerOne, playerTwo) => {
		// this.setState({showScores: true})

		axios.post('https://ukce.danjscott.co.uk/api/game')
			.then((res) => {
				// console.log(res);
				this.setState({
					playerOneName: playerOne, 
					playerTwoName: playerTwo,
					activePlayer: 'player_one',
					gameId: res.data.id,
					showScores: true
				});
			});
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

		axios.post('https://ukce.danjscott.co.uk/api/game/active_player/' + this.state.gameId)
	}

	start = () => {
		let connection = new WebSocket('ws://localhost:8765');
		let msg = 'start#' + this.state.gameId;
		// alert(msg);
		connection.onopen = () => {
			// connection.send('start');
			// alert(msg)
			connection.send(msg);
			setInterval(this.getPoints, 3500);
		}
	}
  
	render() {
		const players = this.state.players || [];
		// console.log(players);
		// console.log(players[1]);
		// console.log(players[1]);
		return (
			<div className="App">
				<Container className="main">

				{/* <Row>
					<Col sm={{size:4, offset: 4}}>
					<div className="score-block">
					<p className="player-name">{this.state.playerOneName}</p>
					<p className="points-counter">{this.state.playerOnePoints}</p>
					</div>
					</Col>
				</Row> */}
				{
					!this.state.showScores && (
						<PlayerNameInput showNextComponent={this.showNextComponent}></PlayerNameInput>
						)
					}
				{
					(this.state.showScores) && (
						<div>
							<Button color="primary" onClick={this.start}>Start</Button>
							<br/>
							<br/>
							<Button color="primary" onClick={this.changePlayer}>Change Player</Button>
							<PlayerScore name={this.state.playerOneName} score={this.state.playerOnePoints}/>
							{/* <PlayerScore name={this.state.players[0].name} score={this.state.players[0].points}/> */}
							<Row></Row>
							{/* <PlayerScore name={this.state.players[0].name} score={this.state.players[0].points}/> */}
							<PlayerScore name={this.state.playerTwoName} score={this.state.playerTwoPoints}/>
							{/* <PlayerScore name={this.state.players[1].name} score={this.state.players[1].points}/> */}
						</div>
					)
				}


				{/* <Row>
					<Col sm={{size:4, offset: 4}}>
						<div className="score-block">
							<p className="player-name">{this.state.playerTwoName}</p>
							<p className="points-counter">{this.state.playerTwoPoints}</p>
						</div>
					</Col>
				</Row> */}
				</Container>
				{/* <header className="App-header">
				<p>
					Edit <code>src/App.js</code> and save to reload.
				</p>
				<a
					className="App-link"
					href="https://reactjs.org"
					target="_blank"
					rel="noopener noreferrer"
				>
					Learn
				</a>
				</header> */}
			</div>
		);
	}
}

export default App;
