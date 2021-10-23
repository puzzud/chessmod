from typing import Any, Dict, List

from engine.observer import Observer
from engine.gamePlayer import GamePlayer

class GameModel(Observer):
	def __init__(self):
		super().__init__()

		self.signalHandlers["commandIssued"] = self.onCommandIssued
		self.signalHandlers["playerJoinRequested"] = self.onPlayerJoinRequested

		self.players: list[GamePlayer] = []

	def initialize(self) -> int:
		self.notify("gameInitialized", {})
		
		self.startGame()

		return 0

	def shutdown(self) -> int:
		return 0
	
	def onCommandIssued(self, command: Dict[str, Any]) -> None:
		commandName: str = command["name"]
		commandName = commandName.lower()
		if commandName == "player_type":
			playerIndex: int = command["index"]
			playerTypeId = int(command["value"])
			self.updatePlayerType(playerIndex, playerTypeId)

	def onPlayerJoinRequested(self, player: GamePlayer) -> None:
		self.addPlayer(player)

	def startGame(self) -> None:
		self.notify("gameStarted")

	def endGame(self) -> None:
		self.notify("gameEnded")
	
	def addPlayer(self, player: GamePlayer) -> None:
		player = player.copy()
		self.players.append(player)

		self.notify("playerAdded", player)
	
	def updatePlayerType(self, playerIndex: int, playerTypeId: int) -> None:
		self.players[playerIndex].typeId = playerTypeId
		self.notify("playerTypeUpdated", {"index": playerIndex, "value": playerTypeId})
	