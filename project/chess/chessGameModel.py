from typing import List

from engine.gameModel import GameModel
import chess.pieceSet
from chess.board import Board

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

		self.board = Board(8, 8, chess.pieceSet.ChessPieceSet())

		self.currentTurnTeamIndex = 0
		self.phaseId = 0
		self.turnStateId = 0
		self.validCellIndices = []
		self.activatedPieceCellIndex = -1

	def getAllKingsOnBoard(self) -> List:
		kingCellIndices = []

		pieceType = self.board.pieceSet.KingPieceType
		for cellIndex in range(len(self.board.cellPieceTypes)):
			if self.board.cellPieceTypes[cellIndex] == pieceType:
				kingCellIndices.append(cellIndex)

		return kingCellIndices

	def initialize(self) -> int:
		self.board.loadFromStringRowList(
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

		return super().initialize()

	def shutdown(self) -> int:
		return super().shutdown()

	def activatePiece(self, cellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
		self.activatedPieceCellIndex = cellIndex
		self.turnStateId = 1
		
		self.notify("pieceActivated", cellIndex)

	def deactivatePiece(self, cellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
		self.activatedPieceCellIndex = -1
		self.turnStateId = 0

		self.notify("pieceDeactivated", cellIndex)

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[fromCellIndex]
		teamIndex = self.board.cellPieceTeams[fromCellIndex]

		self.board.cellPieceTypes[fromCellIndex] = -1
		self.board.cellPieceTeams[fromCellIndex] = -1

		self.board.cellPieceTypes[toCellIndex] = pieceTypeIndex
		self.board.cellPieceTeams[toCellIndex] = teamIndex

		self.activatedPieceCellIndex = -1

		self.notify("pieceMoved", [fromCellIndex, toCellIndex])

	def startTurn(self) -> None:
		self.turnStateId = 0
		self.validCellIndices = []
		self.activatedPieceCellIndex = -1

		self.notify("turnStarted")

	def endTurn(self) -> None:
		self.notify("turnEnded")

		if not self.checkForEndOfGame():
			self.currentTurnTeamIndex = (self.currentTurnTeamIndex + 1) % len(self.teamNames)
			self.startTurn()
	
	def startGame(self) -> None:
		self.currentTurnTeamIndex = 0
		self.phaseId = 0

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
		
		if self.phaseId == 0:
			if self.turnStateId == 0:
				pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
				if pieceTypeIndex != -1:
					teamIndex = self.board.cellPieceTeams[cellIndex]
					if teamIndex == self.currentTurnTeamIndex:
						isValidCell = True
						self.activatePiece(cellIndex)
			elif self.turnStateId == 1:
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
		