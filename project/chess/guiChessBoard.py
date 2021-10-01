from typing import List, Tuple

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
#from gui.guiLabel import GuiLabel

from chess.board import Board

class GuiChessBoard(GuiNode):
	def __init__(self, position: List, board: Board) -> None:
		super().__init__(position)

		self.board = board

		self.cellPixelWidth = 64
		self.cellPixelHeight = 64

		self.cellColors = [
			(192, 192, 192),
			(128, 128, 128)
		]

		self.pieceColors = [
			(255, 255, 255),
			(0, 0, 0)
		]

		pieceCharacterFont = pygame.font.SysFont("", int(self.cellPixelWidth * 1.5))
		self.pieceIconSurfaces = self.renderPieceIconSurfaces(pieceCharacterFont)

		self.boardOverlaySurface = pygame.Surface([self.cellPixelWidth * self.board.cellWidth, self.cellPixelHeight * self.board.cellHeight], pygame.SRCALPHA, 32)
		self.boardOverlaySurface.convert_alpha()
		self.boardOverlaySurface.fill((0, 0, 0, 0))
		
		self.boardOverlayCellStates = [0] * self.board.getNumberOfCells()

		self.surface = pygame.Surface([self.board.cellWidth * self.cellPixelWidth, self.board.cellHeight * self.cellPixelHeight])

		self.render()

	# TODO: Will want to transform from global (parent) space eventually when board is moved out of top left corner.
	def getCellCoordinatesFromPoint(self, position: List) -> List:
		return [
			int(position[0] / self.cellPixelWidth),
			int(position[1] / self.cellPixelHeight)
		]

	def setHighlightedCells(self, activeCellIndex: int, validCellIndices: List) -> None:
		self.boardOverlayCellStates[activeCellIndex] = 1
		
		for validCellIndex in validCellIndices:
			self.boardOverlayCellStates[validCellIndex] = 2
		
		self.renderBoardOverlay()
		self.render()
	
	def clearHighlightedCells(self) -> None:
		self.boardOverlayCellStates = [0] * self.board.getNumberOfCells()

		self.renderBoardOverlay()
		self.render()

	def renderOnSelf(self) -> None:
		self.drawBoard(self.board)
		self.drawPieces(self.board)
	
	def renderPieceIconSurfaces(self, font: pygame.font) -> List:
		pieceIconSurfaces = []

		for teamIndex in range(2):
			teamPieceIconSurfaces = []

			pieceColor = self.pieceColors[teamIndex]
			for pieceIndex in range(len(self.board.pieceSet.pieces)):
				piece = self.board.pieceSet.pieces[pieceIndex]
				pieceIconSurface = font.render(piece.character, True, self.pieceColors[teamIndex])
				teamPieceIconSurfaces.append(pieceIconSurface)
			
			pieceIconSurfaces.append(teamPieceIconSurfaces)

		return pieceIconSurfaces
	
	def renderBoardOverlay(self) -> None:
		for y in range(0, self.board.cellHeight):
			for x in range(0, self.board.cellWidth):
				cellIndex = self.board.getCellIndexFromCoordinates([x, y])
				
				cellColor = None
				if self.boardOverlayCellStates[cellIndex] == 0:
					cellColor = (0, 0, 0, 0)
				else:
					cellColor = (64, 64, 64, 192)
				
				pygame.draw.rect(self.boardOverlaySurface, cellColor, pygame.Rect(x * self.cellPixelWidth, y * self.cellPixelHeight, self.cellPixelWidth, self.cellPixelHeight))

	def drawBoard(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = self.board.getCellIndexFromCoordinates([x, y])
				
				cellColor = None
				if (cellIndex % 2) == (y % 2):
					cellColor = self.cellColors[0]
				else:
					cellColor = self.cellColors[1]

				pygame.draw.rect(self.surface, cellColor, pygame.Rect(x * self.cellPixelWidth, y * self.cellPixelHeight, self.cellPixelWidth, self.cellPixelHeight))
		
		self.drawBoardOverlays()

	def drawBoardOverlays(self) -> None:
		self.surface.blit(self.boardOverlaySurface, (0, 0))

	def drawPieces(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = board.getCellIndexFromCoordinates([x, y])

				cellPieceType = board.cellPieceTypes[cellIndex]
				if cellPieceType is not -1:
					self.drawPiece(self.surface, x, y, cellPieceType, board.cellPieceTeams[cellIndex])

	def drawPiece(self, screen: pygame.Surface, cellX: int, cellY: int, pieceType: int, teamIndex: int) -> None:
		pieceIconSurface = self.pieceIconSurfaces[teamIndex][pieceType]

		cellLeft = cellX * self.cellPixelWidth
		cellTop = cellY * self.cellPixelHeight

		self.surface.blit(pieceIconSurface, (cellLeft, cellTop))
	