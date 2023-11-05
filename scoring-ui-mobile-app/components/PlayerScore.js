import React from "react";
import { StyleSheet, Text, View, Button } from "react-native";

const PlayerScore = (props) => {
	return (
		<View style={styles.scoreBlock}>
			<Text
				style={
					props.active ? styles.playerNameActive : styles.playerName
				}
			>
				{props.name}
			</Text>
			<Text
				style={
					props.active
						? styles.playerPointsActive
						: styles.playerPoints
				}
			>
				{props.score}
			</Text>
		</View>
	);
};

export default PlayerScore;

const styles = StyleSheet.create({
	scoreBlock: {
		alignItems: "center",
	},
	playerName: {
		color: "#fff",
		fontSize: 58,
	},
	playerNameActive: {
		color: "#61dafb",
		fontSize: 58,
	},
	playerPoints: {
		color: "#fff",
		fontSize: 88,
	},
	playerPointsActive: {
		color: "#61dafb",
		fontSize: 88,
	},
	active: {
		color: "#61dafb",
	},
	scoreBtn: {
		height: 10,
	},
});
