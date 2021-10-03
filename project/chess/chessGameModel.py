from typing import List

from enum import Enum

from engine.gameModel import GameModel
import chess.chessPieceSet
from chess.board import ChessBoard

class ChessPhaseId(Enum):
	PLAY = 0

class ChessTurnStateId(Enum):
	PIECE_NOT_ACTIVE = 0
	PIECE_ACTIVE = 1

class ChessGameModel(GameModel):
	def __init__(self):
		super().__init__()

		self.signalHandlers = {
			"cellSelected": self.onCellSelected
		}

		self.teamNames = [
			"White",
			"Black"
		]

		self.board = ChessBoard()

		self.currentTurnTeamIndex = 0
		self.phaseId = ChessPhaseId.PLAY
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE
		self.activatedPieceCellIndex = -1

	def getAllKingsOnBoard(self) -> List:
		kingCellIndices = []

		pieceType = self.board.pieceSet.KingPieceType
		for cellIndex in range(len(self.board.cellPieceTypes)):
			if self.board.cellPieceTypes[cellIndex] == pieceType:
				kingCellIndices.append(cellIndex)

		return kingCellIndices

	def initialize(self) -> int:
		boardStringRowList = [
			"rnbqkbnr",
			"pppppppp",
			"........",
			"........",
			"........",
			"........",
			"PPPPPPPP",
			"RNBQKBNR"
		]

		self.board.loadFromStringRowList(boardStringRowList)

		payload = {
			"teamNames": self.teamNames.copy(),
			"boardStringRowList": boardStringRowList.copy()
		}

		self.notify("gameInitialized", payload)
		
		self.startGame()

		return 0

	def shutdown(self) -> int:
		return super().shutdown()

	def activatePiece(self, cellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
		self.activatedPieceCellIndex = cellIndex
		self.turnStateId = ChessTurnStateId.PIECE_ACTIVE

		payload = {
			"activatedCellIndex": cellIndex,
			"validCellIndices": self.board.getValidMoveCellIndices(cellIndex)
		}

		self.notify("pieceActivated", payload)

	def deactivatePiece(self, cellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
		self.activatedPieceCellIndex = -1
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE

		self.notify("pieceDeactivated", cellIndex)

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> None:
		self.board.movePiece(fromCellIndex, toCellIndex)

		self.activatedPieceCellIndex = -1

		self.notify("pieceMoved", [fromCellIndex, toCellIndex])

	def startTurn(self) -> None:
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE
		self.activatedPieceCellIndex = -1

		self.notify("turnStarted", self.currentTurnTeamIndex)

	def endTurn(self) -> None:
		self.notify("turnEnded")

		if not self.checkForEndOfGame():
			self.currentTurnTeamIndex = (self.currentTurnTeamIndex + 1) % len(self.teamNames)
			self.startTurn()
	
	def startGame(self) -> None:
		self.currentTurnTeamIndex = 0
		self.phaseId = ChessPhaseId.PLAY

		self.notify("gameStarted")

		self.startTurn()

	def endGame(self) -> None:
		winningTeamIndex = self.board.cellPieceTeams[self.getAllKingsOnBoard()[0]]

		self.notify("gameEnded", winningTeamIndex)

	def checkForEndOfGame(self) -> bool:
		if len(self.getAllKingsOnBoard()) == 1:
			self.endGame()
			return True
		
		return False

	def onCellSelected(self, cellIndex: int) -> None:
		isValidCell = False
		
		if self.phaseId == ChessPhaseId.PLAY:
			if self.turnStateId == ChessTurnStateId.PIECE_NOT_ACTIVE:
				pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
				if pieceTypeIndex != -1:
					teamIndex = self.board.cellPieceTeams[cellIndex]
					if teamIndex == self.currentTurnTeamIndex:
						isValidCell = True
						self.activatePiece(cellIndex)
			elif self.turnStateId == ChessTurnStateId.PIECE_ACTIVE:
				if cellIndex == self.activatedPieceCellIndex:
					isValidCell = True
					self.deactivatePiece(cellIndex)
				else:
					isValidCell = self.board.isValidMoveDestination(self.activatedPieceCellIndex, cellIndex)
					if isValidCell:
						self.movePiece(self.activatedPieceCellIndex, cellIndex)
						self.endTurn()

		if not isValidCell:
			self.notify("invalidCellSelected", cellIndex)
	