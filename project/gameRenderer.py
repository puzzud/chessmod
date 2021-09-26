from typing import List

import pygame
from pygame.locals import *

from observer import Observer
from gameLogic import GameLogic

class GameRenderer(Observer):
	from board import Board
	
	def __init__(self, gameLogic: GameLogic):
		super().__init__()

		self.signalHandlers = {
			"gameInitialized": self.onGameInitialized,
			"pointerDown": self.onPointerDown,
			"turnEnded" : self.onTurnEnded,
			"pieceActivated": self.onPieceActivated,
			"pieceDeactivated": self.onPieceDeactivated
		}

		self.gameLogic = gameLogic
		self.attach(gameLogic, "cellSelected")
		gameLogic.attach(self, "gameInitialized")
		gameLogic.attach(self, "turnEnded")
		gameLogic.attach(self, "pieceActivated")
		gameLogic.attach(self, "pieceDeactivated")

		self.cellPixelWidth = 64
		self.cellPixelHeight = 64

		self.backgroundColor = (0, 0, 0)

		self.cellColors = [
			(192, 192, 192),
			(128, 128, 128)
		]

		self.pieceColors = [
			(255, 255, 255),
			(0, 0, 0)
		]

		pygame.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((800, 600))

		self.boardOverlayCellStates = []
		self.boardOverlaySurface = None

		self.pieceIconSurfaces = []
	
	def __del__(self):
		pygame.quit()

	def getCellIndexFromPoint(self, position: List) -> int:
		boardCellWidth = self.gameLogic.board.cellWidth
		
		cellX = int(position[0] / self.cellPixelWidth)
		if cellX >= boardCellWidth:
			return -1

		cellY = int(position[1] / self.cellPixelHeight)
		if cellY >= self.gameLogic.board.cellHeight:
			return -1

		cellIndex = (cellY * boardCellWidth) + cellX
		return cellIndex

	def renderPieceIconSurfaces(self, font) -> List:
		pieceIconSurfaces = []

		for teamIndex in range(2):
			teamPieceIconSurfaces = []

			pieceColor = self.pieceColors[teamIndex]
			for pieceIndex in range(len(self.gameLogic.board.pieceSet.pieces)):
				piece = self.gameLogic.board.pieceSet.pieces[pieceIndex]
				pieceIconSurface = font.render(piece.character, True, self.pieceColors[teamIndex])
				teamPieceIconSurfaces.append(pieceIconSurface)
			
			pieceIconSurfaces.append(teamPieceIconSurfaces)

		return pieceIconSurfaces

	def renderBoardOverlay(self) -> None:
		for y in range(0, self.gameLogic.board.cellHeight):
			for x in range(0, self.gameLogic.board.cellWidth):
				cellIndex = (y * self.gameLogic.board.cellWidth) + x
				
				cellColor = None
				if self.boardOverlayCellStates[cellIndex] == 0:
					cellColor = (0, 0, 0, 0)
				else:
					cellColor = (64, 64, 64, 255)
				
				pygame.draw.rect(self.boardOverlaySurface, cellColor, pygame.Rect(x * self.cellPixelWidth, y * self.cellPixelHeight, self.cellPixelWidth, self.cellPixelHeight))

	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		board = self.gameLogic.board
		self.drawBoard(board)
		self.drawPieces(board)

		pygame.display.update()

	def drawBoard(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = (y * board.cellWidth) + x
				
				cellColor = None
				if (cellIndex % 2) == (y % 2):
					cellColor = self.cellColors[0]
				else:
					cellColor = self.cellColors[1]

				pygame.draw.rect(self.screen, cellColor, pygame.Rect(x * self.cellPixelWidth, y * self.cellPixelHeight, self.cellPixelWidth, self.cellPixelHeight))
		
		self.drawBoardOverlays()

	def drawBoardOverlays(self) -> None:
		self.screen.blit(self.boardOverlaySurface, (0, 0))

	def drawPieces(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = (y * board.cellWidth) + x

				cellPieceType = board.cellPieceTypes[cellIndex]
				if cellPieceType is not -1:
					self.drawPiece(self.screen, x, y, cellPieceType, board.cellPieceTeams[cellIndex])

	def drawPiece(self, screen: pygame.Surface, cellX: int, cellY: int, pieceType: int, teamIndex: int) -> None:
		pieceIconSurface = self.pieceIconSurfaces[teamIndex][pieceType]

		cellLeft = cellX * self.cellPixelWidth
		cellTop = cellY * self.cellPixelHeight

		self.screen.blit(pieceIconSurface, (cellLeft, cellTop))

	def onGameInitialized(self, payload: None) -> None:
		font = pygame.font.SysFont("", int(self.cellPixelWidth * 1.5))
		self.pieceIconSurfaces = self.renderPieceIconSurfaces(font)

		self.boardOverlaySurface = pygame.Surface([self.cellPixelWidth * self.gameLogic.board.cellWidth, self.cellPixelHeight * self.gameLogic.board.cellHeight], pygame.SRCALPHA, 32)
		self.boardOverlaySurface.convert_alpha()
		self.boardOverlaySurface.fill((0, 0, 0, 0))

		numberOfCells = self.gameLogic.board.cellWidth * self.gameLogic.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells

		self.draw()

	def onPointerDown(self, position: List) -> None:
		#print("Pointer Down: " + str(position))
		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.notify("cellSelected", cellIndex)

	def onTurnEnded(self, payload: None) -> None:
		numberOfCells = self.gameLogic.board.cellWidth * self.gameLogic.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells

		self.renderBoardOverlay()
		self.draw()
	
	def onPieceActivated(self, cellIndex) -> None:
		self.boardOverlayCellStates[cellIndex] = 1

		self.renderBoardOverlay()
		self.draw()

	def onPieceDeactivated(self, cellIndex) -> None:
		self.boardOverlayCellStates[cellIndex] = 0
		
		self.renderBoardOverlay()
		self.draw()
	