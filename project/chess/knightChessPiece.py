from typing import Dict, List
import functools

import chess.chessPiece
import chess.chessBoard

class KnightChessPiece(chess.chessPiece.ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveOffsets = [
			[-1, -2],
			[1, -2],
			[2, -1],
			[2, 1],
			[1, 2],
			[-1, 2],
			[-2, 1],
			[-2, -1]
		]

		for moveOffset in moveOffsets:
			moveCellCoordinates = cellCoordinates.copy()
			moveCellCoordinates[0] += moveOffset[0]
			moveCellCoordinates[1] += moveOffset[1]
			if not board.areCellCoordinatesOnBoard(moveCellCoordinates):
				continue

			possibleTargetCellIndices.append(board.getCellIndexFromCoordinates(moveCellCoordinates))

		possibleTargetCellIndices = list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleTargetCellIndices))

		return possibleTargetCellIndices
