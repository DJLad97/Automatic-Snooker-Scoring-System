import React, { Component } from 'react';
import axios from 'axios';
import {Container, Row, Col } from 'reactstrap';
import DigitRoll from 'digit-roll-react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

	constructor(props) {
		super(props);
		this.state = {
			playerOneName: '',
			playerOnePoints: 0,
			playerTwoName: '',
			playerTwoPoints: 0,
		}
		
	}

	getPoints = () => {
		axios.get('https://ukce.danjscott.co.uk/api/player/' + this.state.playerOneName)
			.then((res) => {
				this.setState({playerOnePoints: res.data.points});
			});
	
		axios.get('https://ukce.danjscott.co.uk/api/player/' + this.state.playerTwoName)
			.then((res) => {
				this.setState({playerTwoPoints: res.data.points});

			});
	}
  	componentDidMount(){
		  this.getPlayerNames();
		// this.readDatabase();

		setInterval(this.getPoints, 3500);
	}

	getPlayerNames(){
		let playerOne = 'Dan';
		let playerTwo = 'Ronnie';

		axios.get('https://ukce.danjscott.co.uk/api/player/' + playerOne)
			.then((res) => {
				this.setState({playerOneName: res.data.name});
				this.setState({playerOnePoints: res.data.points});
			});

		axios.get('https://ukce.danjscott.co.uk/api/player/' + playerTwo)
			.then((res) => {
				this.setState({playerTwoName: res.data.name});
				this.setState({playerTwoPoints: res.data.points});
			});
	}
  
	render() {
		return (
			<div className="App">
				<Container className="main">
				<Row>
					<Col sm={{size:4, offset: 4}}>
						<div className="score-block">
							<p className="player-name">{this.state.playerOneName}</p>
							<p className="points-counter">{this.state.playerOnePoints}</p>
						</div>
					</Col>
				</Row>
				<Row></Row>
				<Row>
					<Col sm={{size:4, offset: 4}}>
						<div className="score-block">
							<p className="player-name">{this.state.playerTwoName}</p>
							<p className="points-counter">{this.state.playerTwoPoints}</p>
						</div>
					</Col>
				</Row>
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
