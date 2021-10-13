from typing import Dict, List
import functools

import chess.chessPiece
import chess.rookChessPiece
import chess.chessBoard

class KingChessPiece(chess.chessPiece.ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = self.getPossibleMoveCellIndices(_board, cellIndex)
		possibleTargetCellIndices += self.getPossibleCastleTargetCellIndices(_board, cellIndex)
		return possibleTargetCellIndices

	def getPossibleMoveCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleMoveCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = 1

		moveDirections = [
			[0, -1],
			[1, 0],
			[0, 1],
			[-1, 0],
			[-1, -1],
			[1, -1],
			[-1, 1],
			[1, 1]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleMoveCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))
		
		# TODO: Should result castle move cells be reported here?

		return possibleMoveCellIndices

	def getPossibleAttackCellIndices(self, _board, cellIndex: int) -> List[int]:
		board: chess.chessBoard.ChessBoard = _board
		possibleMoveCellIndices = self.getPossibleMoveCellIndices(board, cellIndex)
		return list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleMoveCellIndices))

	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		if self.isValidCastleTargetCell(board, activeCellIndex, targetCellIndex):
			return self.getPieceActionsFromCastle(board, activeCellIndex, targetCellIndex)

		return super().getPieceActionsFromTargetCell(board, activeCellIndex, targetCellIndex)

	def getPossibleCastleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []
		
		board: chess.chessBoard.ChessBoard = _board

		if self.moveCount == 0:
			rookIndices = board.getAllRookIndices(self.teamIndex)
			for rookIndex in rookIndices:
				if self.isValidCastleTargetCell(board, cellIndex, rookIndex):
					possibleTargetCellIndices.append(rookIndex)
		
		return possibleTargetCellIndices

	def isValidCastleTargetCell(self, _board, cellIndex: int, targetCellIndex: int) -> bool:
		board: chess.chessBoard.ChessBoard = _board
		
		piece = board.getPieceFromCell(cellIndex)
		if piece is None or not isinstance(piece, KingChessPiece):
			return False
		
		if piece.moveCount > 0:
			return False
		
		targetPiece = board.getPieceFromCell(targetCellIndex)
		if targetPiece is None or not isinstance(targetPiece, chess.rookChessPiece.RookChessPiece):
			return False
		
		if targetPiece.moveCount > 0:
			return False
		
		kingCellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)
		rookCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)

		# Must be at same row.
		if kingCellCoordinates[1] != rookCellCoordinates[1]:
			return False

		moveDirection = board.getDirectionBetweenCellCoordinates(kingCellCoordinates, rookCellCoordinates)

		# Check if any of the cells between the king and the rook are not empty.
		rayCellIndices = board.getCellsFromRay(kingCellCoordinates, moveDirection)
		if targetCellIndex not in rayCellIndices:
			return False

		# Check if either of the two cells from the king to the rook would put this king into check.
		if len(rayCellIndices) < 2:
			return False
		
		rayCellIndices = rayCellIndices[:2]
		for rayCellIndex in rayCellIndices:
			if board.doesTargetCellPutTeamKingIntoCheck(cellIndex, rayCellIndex, piece.teamIndex):
				return False

		return True

	def getPieceActionsFromCastle(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		# NOTE: Assumes a castle is possible (isValidCastleTargetCell is True).
		kingCellCoordinates = board.getCellCoordinatesFromIndex(activeCellIndex)
		rookCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)

		moveDirection = board.getDirectionBetweenCellCoordinates(kingCellCoordinates, rookCellCoordinates)
		
		rookCellCoordinates[0] = kingCellCoordinates[0] + moveDirection[0] # Distance 1
		kingCellCoordinates[0] += (moveDirection[0] * 2) # Distance 2

		rookToCellIndex = board.getCellIndexFromCoordinates(rookCellCoordinates)
		kingToCellIndex = board.getCellIndexFromCoordinates(kingCellCoordinates)

		kingMovePieceActions = board.getMovePieceActions(activeCellIndex, kingToCellIndex)
		rookMovePieceActions = board.getMovePieceActions(targetCellIndex, rookToCellIndex)

		return rookMovePieceActions + kingMovePieceActions
	