import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

const PlayerScore = (props) => {
    return (
        <View style={styles.scoreBlock}>
            <Text style={(props.active) ? styles.playerNameActive : styles.playerName}>
                {props.name}
            </Text>
            <Text style={(props.active) ? styles.playerPointsActive : styles.playerPoints}>
                {props.score}
            </Text>
        </View>
    )
}

export default PlayerScore;

const styles = StyleSheet.create({
	scoreBlock: {
		alignItems: 'center',
		// marginTop: 80
	},
	playerName: {
		// font-size: calc(100px + 2vmin);
		color: '#fff',
		fontSize: 78,
		// marginTop: 80
    },
    playerNameActive: {
		// font-size: calc(100px + 2vmin);
		color: '#61dafb',
		fontSize: 78,
		// marginTop: 80
	},
	playerPoints: {
		color: '#fff',
		fontSize: 108,
		// marginTop: 50
    },
    playerPointsActive: {
		color: '#61dafb',
		fontSize: 108,
		// marginTop: 50
    },
    active: {
        color: '#61dafb'
    }
});