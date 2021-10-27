from typing import Any, Dict, List

from engine.observer import Observer
from engine.gameModel import GameModel
from engine.gameController import GameController
from engine.gamePlayer import GamePlayer

class GameView(Observer):
	def __init__(self, gameModel: GameModel, gameController: GameController):
		super().__init__()

		self.signalHandlers["gameQuit"] = self.onGameQuit
		self.signalHandlers["playerAdded"] = self.onPlayerAdded
		self.signalHandlers["playerTypeUpdated"] = self.onPlayerTypeUpdated
		self.signalHandlers["gameEnded"] = self.onGameEnded

		gameModel.attach(self, "gameQuit")
		gameModel.attach(self, "playerAdded")
		gameModel.attach(self, "playerTypeUpdated")
		gameModel.attach(self, "gameEnded")

		self.running = False
	
	def __del__(self):
		pass

	def loop(self) -> int:
		return 0

	def onGameQuit(self, payload: None) -> None:
		pass

	def onPlayerAdded(self, player: GamePlayer) -> None:
		pass
	
	def onPlayerTypeUpdated(self, payload: Dict[str, Any]) -> None:
		pass
	
	def onGameEnded(self, winningTeamIndex: int) -> None:
		self.running = False
	