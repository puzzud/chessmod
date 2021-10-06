from typing import Dict, List

from chess.piece import Piece
import chess.chessBoard

class ChessPiece(Piece):
	def __init__(self, teamIndex: int = -1):
		super().__init__(teamIndex)

		self.hasMoved = False
	
	def __copy__(self):
		chessPieceCopy = ChessPiece(self.teamIndex)
		chessPieceCopy.hasMoved = self.hasMoved
		return chessPieceCopy

class PawnChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		# Move forward
		moveDirection = [0, 1]
		if self.teamIndex == 0:
			moveDirection[1] *= -1
		
		moveDistance = 2 if self.getRank(board, cellCoordinates) == 2 else 1

		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
		possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex), rayCells))
		
		# Attack forward left
		moveDirection[0] = -1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleMoves += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		# Attack forward right
		moveDirection[0] = 1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleMoves += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleMoves
	
	def getRank(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		return board.cellHeight - cellCoordinates[1] if self.teamIndex == 0 else cellCoordinates[1] + 1

class RookChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

		moveDirections = [
			[0, -1],
			[1, 0],
			[0, 1],
			[-1, 0]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleMoves

class KnightChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

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

			possibleMoves.append(board.getCellIndexFromCoordinates(moveCellCoordinates))

		possibleMoves = list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleMoves))

		return possibleMoves

class BishopChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

		moveDirections = [
			[-1, -1],
			[1, -1],
			[-1, 1],
			[1, 1]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleMoves

class QueenChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleMoves

class KingChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		possibleMoves: list[int] = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleMoves
