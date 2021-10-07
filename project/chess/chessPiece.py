from typing import Dict, List

from chess.piece import Piece
import chess.chessBoard

class ChessPiece(Piece):
	def __init__(self, teamIndex: int = -1, moveCount = 0):
		super().__init__(teamIndex, moveCount)
	
	def __copy__(self):
		return ChessPiece(teamIndex = self.teamIndex, moveCount = self.moveCount)

	# Most chess pieces will just use all possible target cells that have
	# opponents in them, as most of them just move.	
	def getPossibleAttackCellIndices(self, _board, cellIndex: int) -> List[int]:
		board: chess.chessBoard.ChessBoard = _board
		possibleTargetCellIndices = self.getPossibleTargetCellIndices(board, cellIndex)
		return list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleTargetCellIndices))

class PawnChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		# Move forward
		moveDirection = [0, 1]
		if self.teamIndex == 0:
			moveDirection[1] *= -1
		
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

		return possibleTargetCellIndices
	
	def getRank(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		return board.cellHeight - cellCoordinates[1] if self.teamIndex == 0 else cellCoordinates[1] + 1

class RookChessPiece(ChessPiece):
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
			[-1, 0]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices

class KnightChessPiece(ChessPiece):
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

class BishopChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

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
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices

class QueenChessPiece(ChessPiece):
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

class KingChessPiece(ChessPiece):
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

	def getPossibleCastleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []
		
		board: chess.chessBoard.ChessBoard = _board

		if self.moveCount == 0:
			rookIndices = board.getAllRookIndices(self.teamIndex)
			for rookIndex in rookIndices:
				if self.isValidCastleTargetCell(cellIndex, rookIndex, board):
					possibleTargetCellIndices.append(rookIndex)
		
		return possibleTargetCellIndices

	def isValidCastleTargetCell(self, cellIndex: int, targetCellIndex: int, _board) -> bool:
		board: chess.chessBoard.ChessBoard = _board
		
		piece = board.getPieceFromCell(cellIndex)
		if piece is not None and isinstance(piece, KingChessPiece):
			if piece.moveCount > 0:
				return False
		
		targetPiece = board.getPieceFromCell(targetCellIndex)
		if targetPiece is not None and isinstance(targetPiece, RookChessPiece):
			if piece.moveCount > 0:
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
		
		kingInCheckDuringMove = False

		board.clearCellContents(cellIndex)

		rayCellIndices = rayCellIndices[:2]
		for rayCellIndex in rayCellIndices:
			# NOTE: Can't use ChessBoard::doesTargetCellPutTeamKingIntoCheck
			# because it will cause infinite recursion.
			# Maybe there is a way to restructure to avoid such.
			board.setCellContents(rayCellIndex, [piece])
			kingInCheckDuringMove = board.isKingInCheck(piece.teamIndex)
			board.clearCellContents(rayCellIndex)
			
			if kingInCheckDuringMove:
				break
		
		board.setCellContents(cellIndex, [piece])

		return not kingInCheckDuringMove
	