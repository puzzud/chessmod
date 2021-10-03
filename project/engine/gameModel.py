from typing import List

from engine.observer import Observer

class GameModel(Observer):
	def __init__(self):
		super().__init__()

	def initialize(self) -> int:
		self.notify("gameInitialized", {})
		
		self.startGame()

		return 0

	def shutdown(self) -> int:
		return 0
	
	def startGame(self) -> None:
		self.notify("gameStarted")

	def endGame(self) -> None:
		self.notify("gameEnded")
	