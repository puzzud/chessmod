from typing import List

import pygame
from pygame.locals import *

from engine.gameView import GameView
from chess.chessGameModel import ChessGameModel

class GuiGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers = {
			"gameInitialized": self.onGameInitialized,
			"pointerDown": self.onPointerDown,
			"turnStarted": self.onTurnStarted,
			"turnEnded" : self.onTurnEnded,
			"pieceActivated": self.onPieceActivated,
			"pieceDeactivated": self.onPieceDeactivated
		}

		self.attach(self.gameModel, "cellSelected")
		self.gameModel.attach(self, "gameInitialized")
		self.gameModel.attach(self, "turnStarted")
		self.gameModel.attach(self, "turnEnded")
		self.gameModel.attach(self, "pieceActivated")
		self.gameModel.attach(self, "pieceDeactivated")

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

		self.playerListFont = None
		self.playerListSurface = None
	
	def __del__(self):
		pygame.quit()

	def getCellIndexFromPoint(self, position: List) -> int:
		boardCellWidth = self.gameModel.board.cellWidth
		
		cellX = int(position[0] / self.cellPixelWidth)
		if cellX >= boardCellWidth:
			return -1

		cellY = int(position[1] / self.cellPixelHeight)
		if cellY >= self.gameModel.board.cellHeight:
			return -1

		cellIndex = (cellY * boardCellWidth) + cellX
		return cellIndex

	def renderPieceIconSurfaces(self, font: pygame.font) -> List:
		pieceIconSurfaces = []

		for teamIndex in range(2):
			teamPieceIconSurfaces = []

			pieceColor = self.pieceColors[teamIndex]
			for pieceIndex in range(len(self.gameModel.board.pieceSet.pieces)):
				piece = self.gameModel.board.pieceSet.pieces[pieceIndex]
				pieceIconSurface = font.render(piece.character, True, self.pieceColors[teamIndex])
				teamPieceIconSurfaces.append(pieceIconSurface)
			
			pieceIconSurfaces.append(teamPieceIconSurfaces)

		return pieceIconSurfaces

	def renderBoardOverlay(self) -> None:
		for y in range(0, self.gameModel.board.cellHeight):
			for x in range(0, self.gameModel.board.cellWidth):
				cellIndex = (y * self.gameModel.board.cellWidth) + x
				
				cellColor = None
				if self.boardOverlayCellStates[cellIndex] == 0:
					cellColor = (0, 0, 0, 0)
				else:
					cellColor = (64, 64, 64, 192)
				
				pygame.draw.rect(self.boardOverlaySurface, cellColor, pygame.Rect(x * self.cellPixelWidth, y * self.cellPixelHeight, self.cellPixelWidth, self.cellPixelHeight))

	def renderPlayerList(self) -> None:
		self.playerListSurface.fill((0, 0, 0, 0))
		
		playerListEntrySize = 64 # TODO: Draw from member.
		
		for teamIndex in range(len(self.gameModel.teamNames)):
			teamName = self.gameModel.teamNames[teamIndex]
			if teamIndex == self.gameModel.currentTurnTeamIndex:
				teamName += " <"

			teamNameSurface = self.playerListFont.render(teamName, True, (255, 255, 255))
			self.playerListSurface.blit(teamNameSurface, (0, playerListEntrySize * teamIndex))
	
	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		board = self.gameModel.board
		self.drawBoard(board)
		self.drawPieces(board)
		self.drawPlayerList()

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
	
	def drawPlayerList(self) -> None:
		self.screen.blit(self.playerListSurface, ((self.cellPixelWidth * self.gameModel.board.cellWidth) + 64, 0))

	def onGameInitialized(self, payload: None) -> None:
		pieceCharacterFont = pygame.font.SysFont("", int(self.cellPixelWidth * 1.5))
		self.pieceIconSurfaces = self.renderPieceIconSurfaces(pieceCharacterFont)

		self.boardOverlaySurface = pygame.Surface([self.cellPixelWidth * self.gameModel.board.cellWidth, self.cellPixelHeight * self.gameModel.board.cellHeight], pygame.SRCALPHA, 32)
		self.boardOverlaySurface.convert_alpha()
		self.boardOverlaySurface.fill((0, 0, 0, 0))

		numberOfCells = self.gameModel.board.cellWidth * self.gameModel.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells

		self.playerListFont = pygame.font.SysFont("", 64)
		self.playerListSurface = pygame.Surface([256, 64 * len(self.gameModel.teamNames)], pygame.SRCALPHA, 32)
		self.playerListSurface.convert_alpha()
		self.playerListSurface.fill((0, 0, 0, 0))

		self.draw()

	def onPointerDown(self, position: List) -> None:
		#print("Pointer Down: " + str(position))
		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.notify("cellSelected", cellIndex)

	def onTurnStarted(self, payload: None) -> None:
		numberOfCells = self.gameModel.board.cellWidth * self.gameModel.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells

		self.renderBoardOverlay()
		self.renderPlayerList()
		self.draw()

	def onTurnEnded(self, payload: None) -> None:
		numberOfCells = self.gameModel.board.cellWidth * self.gameModel.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells

		self.renderBoardOverlay()
		self.draw()
	
	def onPieceActivated(self, cellIndex) -> None:
		for validCellIndex in self.gameModel.board.getValidMoveCellIndices(cellIndex):
			self.boardOverlayCellStates[validCellIndex] = 2

		self.boardOverlayCellStates[cellIndex] = 1

		self.renderBoardOverlay()
		self.draw()

	def onPieceDeactivated(self, cellIndex) -> None:
		numberOfCells = self.gameModel.board.cellWidth * self.gameModel.board.cellHeight
		self.boardOverlayCellStates = [0] * numberOfCells
		
		self.renderBoardOverlay()
		self.draw()
	