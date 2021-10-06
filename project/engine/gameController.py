from typing import List

from engine.observer import Observer
from engine.gameModel import GameModel

class GameController(Observer):
	def __init__(self, gameModel: GameModel):
		super().__init__()

		self.signalHandlers: dict[str, function] = {
			"gameEnded": self.onGameEnded
		}

		gameModel.attach(self, "gameEnded")

		self.running = False
	
	def loop(self) -> int:
		return 0

	def onGameEnded(self, winningTeamIndex: int) -> None:
		self.running = False
