from typing import List

import pygame
from pygame.locals import *

from engine.gameController import GameController
from engine.gameModel import GameModel
from gui.guiGameView import GuiGameView

class GuiGameController(GameController):
	def __init__(self, gameModel: GameModel, guiGameView: GuiGameView):
		super().__init__(gameModel)

		self.eventHandlers = {
			pygame.QUIT: self.onQuitEvent,
			pygame.KEYDOWN: self.onKeyEvent,
			pygame.KEYUP: self.onKeyEvent,
			pygame.MOUSEBUTTONDOWN: self.onMouseEvent,
			pygame.MOUSEBUTTONUP: self.onMouseEvent
		}

		self.attach(guiGameView, "pointerDown")

		self.running = False
	
	def loop(self) -> int:
		self.running = True

		while self.running:
			self.proccessEvents()
		
		return 0

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
	
	def onMouseEvent(self, event: pygame.event) -> None:
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.notify("pointerDown", event.pos)
	