from typing import Dict, List, Set
from enum import Enum

from chess.board import Board, BoardPieceActionType
import chess.pieceSet
import chess.chessPieceSet

class ChessEndGameCondition(Enum):
	NONE = -1
	CHECKMATE = 0
	STALEMATE = 1

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

		return list(filter(lambda cellIndex: isinstance(self.pieceSet.getPieceFromType(self.cellPieceTypes[cellIndex]), chess.chessPieceSet.KingChessPiece), pieceIndices))

	def isKingInCheck(self, teamIndex: int) -> bool:
		# Get combined list of all the valid move destination cell indices of all pieces on the other team.
		allOpponentMoveCellIndices = []

		for opponentTeamPieceIndex in self.getAllOpponentTeamPieces(teamIndex):
			allOpponentMoveCellIndices += super().getValidMoveCellIndices(opponentTeamPieceIndex)

		allOpponentMoveCellIndices = set(allOpponentMoveCellIndices)

		# Is this king's cell index in this list?
		for teamKingCellIndex in self.getAllKingIndices(teamIndex):
			if teamKingCellIndex in allOpponentMoveCellIndices:
				return True

		return False

	def isKingInCheckMate(self, currentTurnTeamIndex: int) -> bool:
		return self.isKingInCheck(currentTurnTeamIndex) and not self.areThereValidMoves(currentTurnTeamIndex)

	def isGameInStalemate(self, currentTurnTeamIndex: int) -> bool:
		if self.isKingInCheck(currentTurnTeamIndex):
			return False

		return not self.areThereValidMoves(currentTurnTeamIndex)

	def getCurrentMetEndOfGameCondition(self, currentTurnTeamIndex: int) -> int:
		if self.isGameInStalemate(currentTurnTeamIndex):
			return ChessEndGameCondition.STALEMATE
		elif self.isKingInCheckMate(currentTurnTeamIndex):
			return ChessEndGameCondition.CHECKMATE
		else:
			return ChessEndGameCondition.NONE

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
	
	def areThereValidMoves(self, teamIndex: int) -> bool:
		allTeamMoveCellIndices = []

		for allTeamMoveCellIndex in self.getAllTeamPieces(teamIndex):
			allTeamMoveCellIndices += self.getValidMoveCellIndices(allTeamMoveCellIndex)

		return (len(allTeamMoveCellIndices) > 0)
	
	def getPieceActionsFromMove(self, fromCellIndex: int, toCellIndex: int) -> List:
		pieceActions = super().getPieceActionsFromMove(fromCellIndex, toCellIndex)

		piece = self.getPieceFromCell(fromCellIndex)
		if isinstance(piece, chess.chessPieceSet.PawnChessPiece):
			pawnPiece: chess.chessPieceSet.PawnChessPiece = piece
			rank = pawnPiece.getRank(self, self.getCellCoordinatesFromIndex(toCellIndex), self.cellPieceTeams[fromCellIndex])
			if rank == 8:
				pieceActions += self.getPieceActionsFromPawnPromotion(toCellIndex, pawnPiece, self.cellPieceTeams[fromCellIndex])
				
		return pieceActions
	
	def getPieceActionsFromPawnPromotion(self, cellIndex: int, pawnPiece: chess.chessPieceSet.PawnChessPiece, teamIndex: int) -> List:
		return [
			{
				"type": BoardPieceActionType.REMOVE_FROM_CELL,
				"cellIndex": cellIndex,
				"pieceType": self.pieceSet.getTypeFromPieceClass(type(pawnPiece)),
				"teamIndex": teamIndex
			},
			{
				"type": BoardPieceActionType.ADD_TO_CELL,
				"cellIndex": cellIndex,
				"pieceType": self.pieceSet.getTypeFromPieceClass(chess.chessPieceSet.QueenChessPiece),
				"teamIndex": teamIndex
			}
		]
