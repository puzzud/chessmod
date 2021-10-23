from typing import List

from engine.observer import Observer
from engine.gameModel import GameModel
from engine.gamePlayer import GamePlayer

class GameView(Observer):
	def __init__(self, gameModel: GameModel):
		super().__init__()

		self.signalHandlers["playerAdded"] = self.onPlayerAdded

		gameModel.attach(self, "playerAdded")
	
	def __del__(self):
		pass

	def onPlayerAdded(self, player: GamePlayer) -> None:
		pass
	