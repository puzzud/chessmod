from typing import Dict, List
import functools

import chess.chessPiece
import chess.chessBoard

class QueenChessPiece(chess.chessPiece.ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

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
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices
