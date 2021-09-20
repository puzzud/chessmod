from typing import List

import pygame
from pygame.locals import *

from observer import Observer
from gameLogic import GameLogic

class GameRenderer(Observer):
	from board import Board
	from pieceTypes import PieceTypes, PieceTypeLetters
	
	def __init__(self, gameLogic: GameLogic):
		super().__init__()

		self.signalHandlers = {
			"gameInitialized": self.onGameInitialized,
			"pointerDown": self.onPointerDown,
			"turnEnded" : self.onTurnEnded
		}

		self.eventHandlers = {
			pygame.QUIT: self.onQuitEvent,
			pygame.KEYDOWN: self.onKeyEvent,
			pygame.KEYUP: self.onKeyEvent,
			pygame.MOUSEBUTTONDOWN: self.onMouseEvent,
			pygame.MOUSEBUTTONUP: self.onMouseEvent
		}

		self.gameLogic = gameLogic
		self.attach(gameLogic, "cellSelected")
		gameLogic.attach(self, "gameInitialized")
		gameLogic.attach(self, "pointerDown")
		gameLogic.attach(self, "turnEnded")

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

		font = pygame.font.SysFont("", int(self.cellPixelWidth * 1.5))
		self.pieceIconSurfaces = self.renderPieceIconSurfaces(font)
	
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
			for pieceTypeIndex in range(self.PieceTypes.NUMBER_OF_TYPES.value):
				pieceIconSurface = font.render(self.PieceTypeLetters[pieceTypeIndex], True, self.pieceColors[teamIndex])
				teamPieceIconSurfaces.append(pieceIconSurface)
			
			pieceIconSurfaces.append(teamPieceIconSurfaces)

		return pieceIconSurfaces

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

	def drawPieces(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = (y * board.cellWidth) + x

				cellPieceType = board.cellPieceTypes[cellIndex]
				if cellPieceType is not self.PieceTypes.NONE.value:
					self.drawPiece(self.screen, x, y, cellPieceType, board.cellPieceTeams[cellIndex])

	def drawPiece(self, screen: pygame.Surface, cellX: int, cellY: int, pieceType: int, teamIndex: int) -> None:
		pieceIconSurface = self.pieceIconSurfaces[teamIndex][pieceType]

		cellLeft = cellX * self.cellPixelWidth
		cellTop = cellY * self.cellPixelHeight

		self.screen.blit(pieceIconSurface, (cellLeft, cellTop))

	def onGameInitialized(self, payload: None) -> None:
		self.draw()
		self.loop()

	def onPointerDown(self, position: List) -> None:
		#print("Pointer Down: " + str(position))
		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.notify("cellSelected", cellIndex)

	def onTurnEnded(self, payload: None) -> None:
		self.draw()
	
	def loop(self) -> int:
		while not self.gameLogic.done:
			self.proccessEvents()

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			eventHandler = self.eventHandlers.get(event.type, None)
			if eventHandler is not None:
				eventHandler(event)
	
	def onQuitEvent(self, event) -> None:
		self.gameLogic.done = True
	
	def onKeyEvent(self, event: pygame.event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.gameLogic.done = True
	
	def onMouseEvent(self, event: pygame.event) -> None:
		if event.type == pygame.MOUSEBUTTONDOWN:
			#self.notify("pointerDown", event.pos)
			self.onPointerDown(event.pos)
	