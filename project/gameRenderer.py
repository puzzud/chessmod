from typing import List

import pygame
from pygame.locals import *

from board import *
from pieceTypes import *

CellPixelWidth = 32
CellPixelHeight = 32

BackgroundColor = (0, 0, 0)

CellColor0 = (192, 192, 192)
CellColor1 = (128, 128, 128)
CellColors = [
	CellColor0,
	CellColor1
]

PieceColor0 = (255, 255, 255)
PieceColor1 = (0, 0, 0)
PieceColors = [
	PieceColor0,
	PieceColor1
]

def renderPieceIconSurfaces(font) -> List:
	pieceIconSurfaces = []

	for teamIndex in range(2):
		teamPieceIconSurfaces = []

		pieceColor = PieceColors[teamIndex]
		for pieceTypeIndex in range(PieceTypes.NUMBER_OF_TYPES.value):
			pieceIconSurface = font.render(PieceTypeLetters[pieceTypeIndex], True, PieceColors[teamIndex])
			teamPieceIconSurfaces.append(pieceIconSurface)
		
		pieceIconSurfaces.append(teamPieceIconSurfaces)

	return pieceIconSurfaces

def drawBoard(screen: pygame.Surface, board: Board) -> None:
	for y in range(0, board.cellHeight):
		for x in range(0, board.cellWidth):
			cellIndex = (y * board.cellWidth) + x
			
			cellColor = None
			if (cellIndex % 2) == (y % 2):
				cellColor = CellColor0
			else:
				cellColor = CellColor1

			pygame.draw.rect(screen, cellColor, pygame.Rect(x * CellPixelWidth, y * CellPixelHeight, CellPixelWidth, CellPixelHeight))

def drawPieces(screen: pygame.Surface, board: Board, pieceIconSurfaces: List) -> None:
	for y in range(0, board.cellHeight):
		for x in range(0, board.cellWidth):
			cellIndex = (y * board.cellWidth) + x

			cellPieceType = board.cellPieceTypes[cellIndex]
			if cellPieceType is not PieceTypes.NONE.value:
				drawPiece(screen, x, y, cellPieceType, board.cellPieceTeams[cellIndex], pieceIconSurfaces)

def drawPiece(screen: pygame.Surface, cellX: int, cellY: int, pieceType: int, teamIndex: int, pieceIconSurfaces: List) -> None:
	pieceIconSurface = pieceIconSurfaces[teamIndex][pieceType]

	cellLeft = cellX * CellPixelWidth
	cellTop = cellY * CellPixelHeight

	screen.blit(pieceIconSurface, (cellLeft, cellTop))
