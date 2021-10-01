from typing import List

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from chess.guiPlayerList import GuiPlayerList
from chess.guiChessBoard import GuiChessBoard

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

		self.chessGameModel = chessGameModel

		self.backgroundColor = (0, 0, 0)

		pygame.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((800, 600))

		self.guiChessBoard: GuiChessBoard = None
		self.guiPlayerList: GuiPlayerList = None
	
	def __del__(self):
		pygame.quit()
		super().__del__()

	def getCellIndexFromPoint(self, position: List) -> int:
		cellCoordinates = self.guiChessBoard.getCellCoordinatesFromPoint(position)
		return self.chessGameModel.board.getCellIndexFromCoordinates(cellCoordinates)
	
	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		self.guiChessBoard.draw(self.screen)
		self.guiPlayerList.draw(self.screen)

		pygame.display.update()

	def onGameInitialized(self, payload: None) -> None:
		self.guiChessBoard = GuiChessBoard([0, 0], self.chessGameModel.board)
		self.guiPlayerList = GuiPlayerList([self.guiChessBoard.getDimensions()[0] + 64, 0], self.chessGameModel.teamNames.copy())

		self.draw()

	def onPointerDown(self, position: List) -> None:
		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.notify("cellSelected", cellIndex)

	def onTurnStarted(self, payload: None) -> None:
		self.guiChessBoard.clearHighlightedCells()
		self.guiPlayerList.setActivePlayerIndex(self.chessGameModel.currentTurnTeamIndex)

		self.draw()

	def onTurnEnded(self, payload: None) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	
	def onPieceActivated(self, cellIndex: int) -> None:
		self.guiChessBoard.setHighlightedCells(cellIndex, self.chessGameModel.board.getValidMoveCellIndices(cellIndex))

		self.draw()

	def onPieceDeactivated(self, cellIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	