import pygame
from pygame.locals import *

from observer import Observer

class GameLogic(Observer):
	from board import Board
	
	def __init__(self):
		super().__init__()

		self.signalHandlers = {
			"cellSelected": self.onCellSelected
		}

		self.eventHandlers = {
			pygame.QUIT: self.onQuitEvent,
			pygame.KEYDOWN: self.onKeyEvent,
			pygame.KEYUP: self.onKeyEvent,
			pygame.MOUSEBUTTONDOWN: self.onMouseEvent,
			pygame.MOUSEBUTTONUP: self.onMouseEvent
		}

		self.done = False

		self.board = self.Board(8, 8)

		self.currentTurnTeamIndex = 0
		self.phaseId = 0
		self.turnStateId = 0

		pygame.init()

	def initialize(self) -> int:
		self.board.loadFromStringRowList(
			[
				"rnbqkbnr",
				"pppppppp",
				"........",
				"........",
				"........",
				"........",
				"PPPPPPPP",
				"RNBQKBNR"
			]
		)

		self.notify("gameInitialized")

		return 0

	def shutdown(self) -> int:
		pygame.quit()

		return 0

	def loop(self) -> int:
		while not self.done:
			self.proccessEvents()

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			eventHandler = self.eventHandlers.get(event.type, None)
			if eventHandler is not None:
				eventHandler(event)
	
	def onQuitEvent(self, event) -> None:
		self.done = True
	
	def onKeyEvent(self, event: pygame.event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True
	
	def onMouseEvent(self, event: pygame.event) -> None:
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.notify("pointerDown", event.pos)
	
	def onCellSelected(self, cellIndex: int) -> None:
		print("Cell Selected: " + str(cellIndex))
