import React, { Component } from 'react';
import { Row, Col } from 'reactstrap';

const PlayerScore = (props) =>{
    return (
    <Row>
        <Col sm={{size:4, offset: 4}}>
            <div className="score-block">
                <p className={(props.active ? "player-name active" : "player-name")}>{props.name}</p>
                <p className={(props.active) ? "points-counter active" : "points-counter"}>{props.score}</p>
            </div>
        </Col>
    </Row>
    );
}

export default PlayerScore;