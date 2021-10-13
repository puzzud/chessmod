from typing import Dict, List, Set
from enum import Enum

from chess.board import Board, BoardPieceActionType
import chess.chessPieceSet
import chess.rookChessPiece
import chess.kingChessPiece

class ChessEndGameCondition(Enum):
	NONE = -1
	CHECKMATE = 0
	STALEMATE = 1

class ChessBoard(Board):
	def __init__(self):
		super().__init__(8, 8, chess.chessPieceSet.ChessPieceSet())

	def getDifferenceBetweenCellCoordinates(self, cellCoordinatesA: List[int], cellCoordinatesB: List[int]) -> List[int]:
		return [
			cellCoordinatesB[0] - cellCoordinatesA[0],
			cellCoordinatesB[1] - cellCoordinatesA[1]
		]
	
	def getDistanceBetweenCellCoordinates(self, cellCoordinatesA: List[int], cellCoordinatesB: List[int]) -> List[int]:
		difference = self.getDifferenceBetweenCellCoordinates(cellCoordinatesA, cellCoordinatesB)
		return [
			abs(difference[0]),
			abs(difference[1])
		]

	def getDirectionBetweenCellCoordinates(self, cellCoordinatesA: List[int], cellCoordinatesB: List[int]) -> List[int]:
		difference = self.getDifferenceBetweenCellCoordinates(cellCoordinatesA, cellCoordinatesB)
		return [
			int(0 if difference[0] == 0 else difference[0] / abs(difference[0])),
			int(0 if difference[1] == 0 else difference[1] / abs(difference[1]))
		]

	def getDirectionBetweenCellIndices(self, cellIndexA: int, cellIndexB: int) -> List[int]:
		cellCoordinatesA = self.getCellCoordinatesFromIndex(cellIndexA)
		cellCoordinatesB = self.getCellCoordinatesFromIndex(cellIndexB)

		return self.getDirectionBetweenCellCoordinates(cellCoordinatesA, cellCoordinatesB)

	def getCellsFromRay(self, sourceCellCoordinates: List[int], direction: List[int], distance: int = -1) -> List[int]:
		cellIndices: list[int] = []
		
		if distance < 0:
			distance = max(self.cellWidth, self.cellHeight)

		cellCoordinates = sourceCellCoordinates.copy()

		for offset in range(distance):
			cellCoordinates[0] += direction[0]
			cellCoordinates[1] += direction[1]
			if not self.areCellCoordinatesOnBoard(cellCoordinates):
				break

			cellIndex = self.getCellIndexFromCoordinates(cellCoordinates)

			cellIndices.append(cellIndex)

			# Stop after meeting a piece.
			if not self.isCellEmpty(cellIndex):
				break
		
		return cellIndices

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

		return list(filter(lambda cellIndex: isinstance(self.getPieceFromCell(cellIndex), chess.kingChessPiece.KingChessPiece), pieceIndices))
	
	def getAllRookIndices(self, teamIndex: int = -1) -> List[int]:
		pieceIndices: list[int] = []

		if teamIndex > -1:
			pieceIndices = self.getAllTeamPieceIndices(teamIndex)
		else:
			pieceIndices = self.getAllPieceIndices()

		return list(filter(lambda cellIndex: isinstance(self.getPieceFromCell(cellIndex), chess.rookChessPiece.RookChessPiece), pieceIndices))

	def isKingInCheck(self, teamIndex: int) -> bool:
		# Get combined list of all the valid attack based destination cell indices of all pieces on the other team.
		allOpponentAttackCellIndices: list[int] = []

		for opponentTeamPieceIndex in self.getAllOpponentTeamPieceIndices(teamIndex):
			allOpponentAttackCellIndices += self.getValidAttackCellIndices(opponentTeamPieceIndex)

		allOpponentAttackCellIndices = list(set(allOpponentAttackCellIndices))

		# Is this king's cell index in this list?
		for teamKingCellIndex in self.getAllKingIndices(teamIndex):
			if teamKingCellIndex in allOpponentAttackCellIndices:
				return True

		return False

	def getCurrentMetEndOfGameCondition(self, currentTurnTeamIndex: int) -> int:
		isKingInCheck = self.isKingInCheck(currentTurnTeamIndex)
		areThereValidMoves = self.areThereValidMoves(currentTurnTeamIndex)

		if not isKingInCheck and not areThereValidMoves:
			return ChessEndGameCondition.STALEMATE
		elif not areThereValidMoves:
			return ChessEndGameCondition.CHECKMATE
		else:
			return ChessEndGameCondition.NONE

	def getValidTargetCellIndices(self, cellIndex: int) -> List[int]:
		piece = self.getPieceFromCell(cellIndex)
		if piece is None:
			print("getValidTargetCellIndices: Error")
			return []
		
		validTargetCellIndices = super().getValidTargetCellIndices(cellIndex)
		teamIndex = piece.teamIndex

		return list(filter(lambda targetCellIndex: not self.doesTargetCellPutTeamKingIntoCheck(cellIndex, targetCellIndex, teamIndex), validTargetCellIndices))

	def doesTargetCellPutTeamKingIntoCheck(self, activeCellIndex: int, targetCellIndex: int, teamIndex: int) -> bool:
		# Temporarily make move.
		pieceActions = self.performPieceAction(activeCellIndex, targetCellIndex)
		
		putsTeamKingIntoCheck = self.isKingInCheck(teamIndex)
		
		self.rollbackPieceActions(pieceActions)

		return putsTeamKingIntoCheck
	
	def areThereValidMoves(self, teamIndex: int) -> bool:
		allTeamValidTargetCellIndices: list[int] = []

		for cellIndex in self.getAllTeamPieceIndices(teamIndex):
			allTeamValidTargetCellIndices += self.getValidTargetCellIndices(cellIndex)

		return (len(allTeamValidTargetCellIndices) > 0)
	