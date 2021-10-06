from typing import Dict, List, Set
from enum import Enum

from chess.board import Board, BoardPieceActionType
import chess.piece
import chess.chessPieceSet
import chess.chessPiece

class ChessEndGameCondition(Enum):
	NONE = -1
	CHECKMATE = 0
	STALEMATE = 1

class ChessBoard(Board):
	def __init__(self):
		super().__init__(8, 8, chess.chessPieceSet.ChessPieceSet())

	def getAllPieceIndices(self) -> List[int]:
		allPieceCellIndices: list[int] = []

		for cellIndex in range(self.getNumberOfCells()):
			if not self.isCellEmpty(cellIndex):
				allPieceCellIndices.append(cellIndex)

		return allPieceCellIndices

	def getAllTeamPieceIndices(self, teamIndex: int) -> List[int]:
		return list(filter(lambda cellIndex: self.getPieceFromCell(cellIndex).teamIndex == teamIndex, self.getAllPieceIndices()))

	def getAllOpponentTeamPieceIndices(self, teamIndex: int) -> List[int]:
		return list(filter(lambda cellIndex: self.getPieceFromCell(cellIndex).teamIndex != teamIndex, self.getAllPieceIndices()))

	def getAllKingIndices(self, teamIndex: int = -1) -> List[int]:
		pieceIndices: list[int] = []

		if teamIndex > -1:
			pieceIndices = self.getAllTeamPieceIndices(teamIndex)
		else:
			pieceIndices = self.getAllPieceIndices()

		return list(filter(lambda cellIndex: isinstance(self.getPieceFromCell(cellIndex), chess.chessPiece.KingChessPiece), pieceIndices))

	def isKingInCheck(self, teamIndex: int) -> bool:
		# Get combined list of all the valid move destination cell indices of all pieces on the other team.
		allOpponentMoveCellIndices: list[int] = []

		for opponentTeamPieceIndex in self.getAllOpponentTeamPieceIndices(teamIndex):
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

	def getValidMoveCellIndices(self, fromCellIndex: int) -> List[int]:
		validMoveCellIndices = super().getValidMoveCellIndices(fromCellIndex)
		teamIndex = self.getPieceFromCell(fromCellIndex).teamIndex

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
		allTeamMoveCellIndices: list[int] = []

		for allTeamMoveCellIndex in self.getAllTeamPieceIndices(teamIndex):
			allTeamMoveCellIndices += self.getValidMoveCellIndices(allTeamMoveCellIndex)

		return (len(allTeamMoveCellIndices) > 0)
	
	def getPieceActionsFromMove(self, fromCellIndex: int, toCellIndex: int) -> List[dict]:
		pieceActions = super().getPieceActionsFromMove(fromCellIndex, toCellIndex)

		piece = self.getPieceFromCell(fromCellIndex)
		if isinstance(piece, chess.chessPiece.PawnChessPiece):
			pawnPiece: chess.chessPiece.PawnChessPiece = piece
			teamIndex = pawnPiece.teamIndex
			rank = pawnPiece.getRank(self, self.getCellCoordinatesFromIndex(toCellIndex), teamIndex)
			if rank == 8:
				pieceActions += self.getPieceActionsFromPawnPromotion(toCellIndex, pawnPiece, teamIndex)
				
		return pieceActions
	
	def getPieceActionsFromPawnPromotion(self, cellIndex: int, piece: chess.piece.Piece, teamIndex: int) -> List[dict]:
		pawnPiece: chess.chessPiece.PawnChessPiece = piece
		
		return [
			{
				"type": BoardPieceActionType.REMOVE_FROM_CELL,
				"cellIndex": cellIndex,
				"pieceTypeId": self.pieceSet.getTypeIdFromPieceType(type(pawnPiece)),
				"teamIndex": teamIndex
			},
			{
				"type": BoardPieceActionType.ADD_TO_CELL,
				"cellIndex": cellIndex,
				"pieceTypeId": self.pieceSet.getTypeIdFromPieceType(chess.chessPiece.QueenChessPiece),
				"teamIndex": teamIndex
			}
		]
