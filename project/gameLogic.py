import pygame
from pygame.locals import *

from observer import Observer

class GameLogic(Observer):
	from board import Board
	
	def __init__(self):
		super().__init__()

		self.done = False

		self.processHandlers = {
			pygame.QUIT: self.processQuitEvent,
			pygame.KEYDOWN: self.processKeyEvent,
			pygame.KEYUP: self.processKeyEvent
		}

		self.board = self.Board(8, 8)

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

		self.notify(0) # TODO: Do enum or string.

		return 0

	def shutdown(self) -> int:
		pygame.quit()

		return 0

	def loop(self) -> int:
		while not self.done:
			self.proccessEvents()

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			processHandler = self.processHandlers.get(event.type, None)
			if processHandler is not None:
				processHandler(event)
	
	def processQuitEvent(self, event) -> None:
		self.done = True
	
	def processKeyEvent(self, event: pygame.event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True
			