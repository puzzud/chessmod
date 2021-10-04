from typing import Dict, List

from chess.board import Board
import chess.pieceSet

class ChessBoard(Board):
	def __init__(self):
		super().__init__(8, 8, chess.chessPieceSet.ChessPieceSet())

	def getAllPieces(self) -> List:
		allPieceCellIndices = []

		for cellIndex in range(self.getNumberOfCells()):
			if self.cellPieceTypes[cellIndex] != -1:
				allPieceCellIndices.append(cellIndex)

		return allPieceCellIndices

	def getAllTeamPieces(self, teamIndex: int) -> List:
		return list(filter(lambda cellIndex: self.cellPieceTeams[cellIndex] == teamIndex, self.getAllPieces()))

	def getAllOpponentTeamPieces(self, teamIndex: int) -> List:
		return list(filter(lambda cellIndex: self.cellPieceTeams[cellIndex] != teamIndex, self.getAllPieces()))

	def getAllKingIndices(self, teamIndex: int = -1) -> List:
		pieceIndices = []

		if teamIndex > -1:
			pieceIndices = self.getAllTeamPieces(teamIndex)
		else:
			pieceIndices = self.getAllPieces()

		return list(filter(lambda cellIndex: self.cellPieceTypes[cellIndex] == self.pieceSet.KingPieceType, pieceIndices))

	def isKingInCheck(self, teamIndex: int) -> bool:
		teamKingCellIndices = self.getAllKingIndices(teamIndex)
		if len(teamKingCellIndices) < 1:
			return False

		# Get combined list of all the valid move destination cell indices of all pieces on the other team.
		allOpponentMoveCellIndices = []

		for opponentTeamPieceIndex in self.getAllOpponentTeamPieces(teamIndex):
			allOpponentMoveCellIndices += super().getValidMoveCellIndices(opponentTeamPieceIndex)

		allOpponentMoveCellIndices = set(allOpponentMoveCellIndices)

		# Is this king's cell index in this list?
		for teamKingCellIndex in teamKingCellIndices:
			if teamKingCellIndex in allOpponentMoveCellIndices:
				return True

		return False

	def getValidMoveCellIndices(self, fromCellIndex: int) -> List:
		validMoveCellIndices = super().getValidMoveCellIndices(fromCellIndex)
		teamIndex = self.cellPieceTeams[fromCellIndex]

		return list(filter(lambda toCellIndex: not self.doesMovePutTeamKingIntoCheck(fromCellIndex, toCellIndex, teamIndex), validMoveCellIndices))

	def doesMovePutTeamKingIntoCheck(self, fromCellIndex: int, toCellIndex: int, teamIndex: int) -> bool:
		# Temporarily make move.
		pieceActions = self.movePiece(fromCellIndex, toCellIndex)
		
		putsTeamKingIntoCheck = self.isKingInCheck(teamIndex)
		
		# Reverse temporary move to restore board state.
		self.reversePieceActions(pieceActions)
		self.executePieceActions(pieceActions)

		return putsTeamKingIntoCheck