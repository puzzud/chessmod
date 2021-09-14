from typing import Dict, List
from enum import Enum

import pygame
from pygame.locals import *

from board import *
from pieceTypes import *
import gameRenderer

BoardCellWidth = 8
BoardCellHeight = 8

def main() -> None:
	pygame.init()
	pygame.font.init()

	done = False

	screen = pygame.display.set_mode((640, 480))
	font = pygame.font.SysFont("", int(gameRenderer.CellPixelWidth * 1.5))

	pieceIconSurfaces = gameRenderer.renderPieceIconSurfaces(font)

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
		
		screen.fill(gameRenderer.BackgroundColor)

		gameRenderer.drawBoard(screen, board)
		gameRenderer.drawPieces(screen, board, pieceIconSurfaces)
		
		pygame.display.update()
	
	pygame.quit()

main()
