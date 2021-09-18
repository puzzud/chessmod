import pygame
from pygame.locals import *

class GameLogic:
	from board import Board
	
	def __init__(self):
		self.done = False

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

	def shutdown(self):
		pygame.quit()

	def proccessEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				self.done = True
	