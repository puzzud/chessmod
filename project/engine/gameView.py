from typing import List

from engine.observer import Observer
from engine.gameModel import GameModel

class GameView(Observer):
	def __init__(self, gameModel: GameModel):
		super().__init__()
	
	def __del__(self):
		pass
