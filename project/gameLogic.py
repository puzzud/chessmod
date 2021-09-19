import pygame
from pygame.locals import *

class GameLogic:
	from board import Board
	
	def __init__(self):
		self.done = False

		self.processHandlers = {
			pygame.QUIT: self.processQuitEvent,
			pygame.KEYDOWN: self.processKeyEvent
		}

		self.board = self.Board(8, 8)
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

		pygame.init()

	def shutdown(self) -> None:
		pygame.quit()

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			processHandler = self.processHandlers.get(event.type, None)
			if processHandler is not None:
				processHandler(event)
	
	def processQuitEvent(self, event) -> None:
		self.done = True
	
	def processKeyEvent(self, event) -> None:
		self.done = True
	