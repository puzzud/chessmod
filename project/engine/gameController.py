from typing import List

from engine.observer import Observer
from engine.gameModel import GameModel
from engine.gamePlayer import GamePlayer

class GameController(Observer):
	def __init__(self, gameModel: GameModel):
		super().__init__()

		self.signalHandlers["playerJoinRequested"] = self.onPlayerJoinRequested

		self.attach(gameModel, "commandIssued")
		self.attach(gameModel, "playerJoinRequested")

	def onPlayerJoinRequested(self, player: GamePlayer) -> None:
		self.notify("playerJoinRequested", player)
	