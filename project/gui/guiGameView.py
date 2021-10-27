from typing import Any, Dict, List

import pygame
from pygame.locals import *

from engine.gameModel import GameModel
from engine.gameController import GameController
from engine.gameView import GameView

from gui.guiNode import GuiNode

class GuiGameView(GameView):
	def __init__(self, gameModel: GameModel, gameController: GameController):
		super().__init__(gameModel, gameController)

		self.signalHandlers["gameInitialized"] = self.onGameInitialized
		self.signalHandlers["commandLineEntered"] = self.onCommandLineEntered

		self.eventHandlers: dict[str, function] = {
			pygame.QUIT: self.onQuitEvent,
			pygame.KEYDOWN: self.onKeyEvent,
			pygame.KEYUP: self.onKeyEvent,
			pygame.MOUSEBUTTONDOWN: self.onMouseEvent,
			pygame.MOUSEBUTTONUP: self.onMouseEvent
		}

		gameModel.attach(self, "gameInitialized")

		self.backgroundColor = (0, 0, 0)

		pygame.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((800, 600))

		self.guiNodes: list[GuiNode] = []
	
	def __del__(self):
		pygame.quit()
		super().__del__()

	def loop(self) -> int:
		self.running = True

		while self.running:
			self.proccessEvents()
			self.process()
		
		return 0

	def process(self) -> None:
		pass

	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		for guiNode in self.guiNodes:
			guiNode.draw(self.screen)

		pygame.display.update()

	def onGameInitialized(self, payload: Dict[str, Any]) -> None:
		pass

	def onGameQuit(self, payload: None) -> None:
		self.running = False

	def onCommandLineEntered(self, textCommand: str) -> None:
		self.notify("textCommandIssued", textCommand)

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			eventHandler = self.eventHandlers.get(event.type, None)
			if eventHandler is not None:
				eventHandler(event)
	
	def onQuitEvent(self, event) -> None:
		self.running = False
	
	def onKeyEvent(self, event: pygame.event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
				return
			
			self.onKeyDown(event.key, event.unicode)
	
	def onKeyDown(self, keyCode: int, character: str) -> None:
		pass

	def onMouseEvent(self, event: pygame.event) -> None:
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.onPointerDown(event.pos)
	
	def onPointerDown(self, position: List[int]) -> None:
		pass
