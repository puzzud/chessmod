from typing import Any, Dict, List

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from chess.guiPlayerList import GuiPlayerList
from chess.guiChessBoard import GuiChessBoard

from engine.gameView import GameView
from chess.chessGameModel import ChessGameModel
from chess.chessBoard import ChessBoard

class GuiGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers: dict[str, function] = {
			"gameInitialized": self.onGameInitialized,
			"pointerDown": self.onPointerDown,
			"turnStarted": self.onTurnStarted,
			"turnEnded" : self.onTurnEnded,
			"pieceActivated": self.onPieceActivated,
			"pieceDeactivated": self.onPieceDeactivated,
			"pieceMoved": self.onPieceMoved
		}

		self.attach(chessGameModel, "cellSelected")
		
		chessGameModel.attach(self, "gameInitialized")
		chessGameModel.attach(self, "turnStarted")
		chessGameModel.attach(self, "turnEnded")
		chessGameModel.attach(self, "pieceActivated")
		chessGameModel.attach(self, "pieceDeactivated")
		chessGameModel.attach(self, "pieceMoved")

		self.backgroundColor = (0, 0, 0)

		pygame.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((800, 600))

		self.guiChessBoard: GuiChessBoard = None
		self.guiPlayerList: GuiPlayerList = None
	
	def __del__(self):
		pygame.quit()
		super().__del__()

	def getCellIndexFromPoint(self, position: List[int]) -> int:
		cellCoordinates = self.guiChessBoard.getCellCoordinatesFromPoint(position)
		return self.guiChessBoard.board.getCellIndexFromCoordinates(cellCoordinates)
	
	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		self.guiChessBoard.draw(self.screen)
		self.guiPlayerList.draw(self.screen)

		pygame.display.update()

	def onGameInitialized(self, payload: Dict[str, Any]) -> None:
		board = ChessBoard()
		board.loadFromStringRowList(payload["boardStringRowList"])
		self.guiChessBoard = GuiChessBoard([0, 0], board)

		self.guiPlayerList = GuiPlayerList([self.guiChessBoard.getDimensions()[0] + 64, 0], payload["teamNames"].copy())

		self.draw()

	def onPointerDown(self, position: List[int]) -> None:
		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.notify("cellSelected", cellIndex)

	def onTurnStarted(self, currentTurnTeamIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()
		self.guiPlayerList.setActivePlayerIndex(currentTurnTeamIndex)

		self.draw()

	def onTurnEnded(self, currentTurnTeamIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	
	def onPieceActivated(self, payload: Dict[str, Any]) -> None:
		self.guiChessBoard.setHighlightedCells(payload["activatedCellIndex"], payload["validCellIndices"])

		self.draw()

	def onPieceDeactivated(self, cellIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	
	def onPieceMoved(self, payload: List[int]) -> None:
		self.guiChessBoard.board.movePiece(payload[0], payload[1])

		self.draw()
