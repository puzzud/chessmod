from typing import Dict, List
import functools

import chess.chessBoard

import chess.chessPiece
import chess.queenChessPiece
import chess.chessBoard

class PawnChessPiece(chess.chessPiece.ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		# Move forward
		moveDirection = self.getPrimaryDirection()
		
		moveDistance = 2 if self.getRank(board, cellCoordinates) == 2 else 1

		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex), rayCells))
		
		# Attack forward left
		moveDirection[0] = -1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		# Attack forward right
		moveDirection[0] = 1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		# Check for en passant.
		enPassantTargetCellIndex = self.getEnPassantTargetCellIndex(_board, cellCoordinates)
		if enPassantTargetCellIndex > -1:
			possibleTargetCellIndices.append(enPassantTargetCellIndex)

		return possibleTargetCellIndices
	
	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		if targetCellIndex == self.getEnPassantTargetCellIndex(board, board.getCellCoordinatesFromIndex(activeCellIndex)):
			return self.getPieceActionsFromEnPassant(board, activeCellIndex, targetCellIndex)

		# Check for promotion.
		pieceActions = board.getMovePieceActions(activeCellIndex, targetCellIndex)
		if self.getRank(board, board.getCellCoordinatesFromIndex(targetCellIndex)) == 8:
			pieceActions += self.getPieceActionsFromPawnPromotion(board, targetCellIndex)
				
		return pieceActions

	def getPrimaryDirection(self) -> List[int]:
		direction = [0, 1]
		if self.teamIndex == 0:
			direction[1] *= -1
		
		return direction

	def getRank(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		return board.cellHeight - cellCoordinates[1] if self.teamIndex == 0 else cellCoordinates[1] + 1

	def getEnPassantTargetCellIndex(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		
		# Get last piece to move.
		numberOfPieceActionsInHistory = len(board.pieceActionHistory)
		if numberOfPieceActionsInHistory == 0:
			return -1
		
		lastPieceAction = board.pieceActionHistory[numberOfPieceActionsInHistory - 1]
		
		if lastPieceAction["type"] != chess.chessBoard.BoardPieceActionType.MOVE_TO_CELL:
			return -1

		# It needs to be a pawn.
		lastMovedPieceTypeId = lastPieceAction["pieceTypeId"]
		if lastMovedPieceTypeId != board.pieceSet.getTypeIdFromPieceType(PawnChessPiece):
			return -1

		# It cannot have moved more than once.
		lastMovedPieceCellIndex = lastPieceAction["toCellIndex"]
		lastMovedPawn: PawnChessPiece = board.getPieceFromCell(lastMovedPieceCellIndex)
		if lastMovedPawn.moveCount > 1:
			return -1

		# It needs to be at rank 4.
		# TODO: Is it better to make sure its only moved 2 cells at once
		# (checking fromCellIndex and vertical distance),
		# in order to allow for alternate starting piece formations?
		# Would want to change associated logic with first move rules to match.
		lastMovedPieceCellCoordinates = board.getCellCoordinatesFromIndex(lastMovedPieceCellIndex)
		if lastMovedPawn.getRank(board, lastMovedPieceCellCoordinates) != 4:
			return -1

		# It needs to be directly to the left or right of this pawn.
		distance = board.getDistanceBetweenCellCoordinates(cellCoordinates, lastMovedPieceCellCoordinates)
		if distance[1] > 0 or distance[0] > 1:
			return -1

		# Pawn move & en passant rules implicate that the cell directly behind
		# the captured pawn will be empty.
		# Assume it's a legit cell that can be moved into.
		primaryDirection = self.getPrimaryDirection()
		enPassantToCoordinates = [
			lastMovedPieceCellCoordinates[0],
			lastMovedPieceCellCoordinates[1] + primaryDirection[1]
		]
		
		return board.getCellIndexFromCoordinates(enPassantToCoordinates)

	def getPieceActionsFromEnPassant(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board
		
		# NOTE: Assumes en passant is possible.
		pawnFromCellCoordinates = board.getCellCoordinatesFromIndex(activeCellIndex)
		pawnToCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)
		otherPawnCellCoordinates = [
			pawnToCellCoordinates[0],
			pawnFromCellCoordinates[1]
		]

		otherPawnRemovePieceActions = board.getRemovePieceActions(board.getCellIndexFromCoordinates(otherPawnCellCoordinates))
		movePawnPieceActions = board.getMovePieceActions(activeCellIndex, targetCellIndex)

		return otherPawnRemovePieceActions + movePawnPieceActions

	def getPieceActionsFromPawnPromotion(self, _board, cellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		pieceActions = board.getRemovePieceActions(cellIndex, board.pieceSet.getTypeIdFromPieceType(type(self)))
		
		pieceAttributes = {
				"teamIndex": self.teamIndex
			}
		
		pieceActions += board.getAddPieceActions(cellIndex, board.pieceSet.getTypeIdFromPieceType(chess.queenChessPiece.QueenChessPiece), pieceAttributes)

		return pieceActions
