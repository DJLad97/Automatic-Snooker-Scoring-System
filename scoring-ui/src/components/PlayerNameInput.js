import React, { Component } from 'react';
import { Button, Input, Label, Row, Col } from 'reactstrap'; 
import axios from 'axios';

class PlayerNameInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            playerOneName: '',
            playerTwoName: ''
        }
    }

    onChange  = (e) => {
        this.setState({[e.target.name]: e.target.value});
    }

    submitNames = () => {
        let playerNames = {
            "player_names": [this.state.playerOneName, this.state.playerTwoName]
        }
        let playerOne = this.state.playerOneName;
        let playerTwo = this.state.playerTwoName;
        this.props.showNextComponent(playerOne, playerTwo);

    }
    
    render() {
        return (
            <div>
                <br/>
                <br/>
                <br/>
                <Row>
                    <Col xs={{span:4, offset:2}} sm={{span:4, offset:2}}>
                        <Label for="playerOneName">Player One Name:</Label>
                        <Input type="text" onChange={this.onChange} name="playerOneName" placeholder="Name" />
                    </Col>
                </Row>
                <Row></Row>
                <Row>
                    <Col xs={{span:4, offset:2}} sm={{span:4, offset:2}}>
                        <Label for="playerTwoName">Player Two Name:</Label>
                        <Input type="text" onChange={this.onChange} name="playerTwoName" placeholder="Name" />
                    </Col>
                </Row>
                <br/>
                <Row>
                    <Col xs={{span:4, offset:4}} sm={{span:4, offset:4}}>
                        <Button color="primary" onClick={this.submitNames}>Submit</Button>
                    </Col>
                </Row>
            </div>
        );
    }
}

export default PlayerNameInput;