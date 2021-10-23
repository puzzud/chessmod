from typing import Any, Dict, List

from engine.observer import Observer
from engine.gameModel import GameModel
from engine.gamePlayer import GamePlayer

class GameView(Observer):
	def __init__(self, gameModel: GameModel):
		super().__init__()

		self.signalHandlers["playerAdded"] = self.onPlayerAdded
		self.signalHandlers["playerTypeUpdated"] = self.onPlayerTypeUpdated
		
		gameModel.attach(self, "playerAdded")
		gameModel.attach(self, "playerTypeUpdated")
	
	def __del__(self):
		pass

	def onPlayerAdded(self, player: GamePlayer) -> None:
		pass
	
	def onPlayerTypeUpdated(self, payload: Dict[str, Any]) -> None:
		pass
	