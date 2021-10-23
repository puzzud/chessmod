from typing import List

from engine.observer import Observer
from engine.gamePlayer import GamePlayer

class GameModel(Observer):
	def __init__(self):
		super().__init__()

		self.signalHandlers["playerJoinRequested"] = self.onPlayerJoinRequested

		self.players: list[GamePlayer] = []

	def initialize(self) -> int:
		self.notify("gameInitialized", {})
		
		self.startGame()

		return 0

	def shutdown(self) -> int:
		return 0
	
	def onPlayerJoinRequested(self, player: GamePlayer) -> None:
		self.addPlayer(player)

	def startGame(self) -> None:
		self.notify("gameStarted")

	def endGame(self) -> None:
		self.notify("gameEnded")
	
	def addPlayer(self, player: GamePlayer) -> None:
		self.notify("playerAdded", player)
	