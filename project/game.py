from typing import Dict, List
from enum import Enum

import pygame
from pygame.locals import *

from board import *
from pieceTypes import *
from gameRenderer import GameRenderer

BoardCellWidth = 8
BoardCellHeight = 8

def main() -> None:
	pygame.init()
	pygame.font.init()

	done = False

	gameRenderer = GameRenderer()
	
	board = Board(BoardCellWidth, BoardCellHeight)
	board.loadFromStringRowList(
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

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				done = True

		gameRenderer.draw(board)
	
	pygame.quit()

main()
