from typing import Dict, List

from chess.piece import Piece
from chess.board import Board

class PieceSet():
	def __init__(self):
		self.pieces = []
	
	def getPiecePropertiesFromCharacter(self, character: str) -> Dict:
		return {
			"pieceType": self.getPieceTypeFromCharacter(character),
			"teamIndex": self.getTeamIndexFromCharacter(character)
		}
	
	def getPieceTypeFromCharacter(self, character: str) -> int:
		return -1

	def getTeamIndexFromCharacter(self, character: str) -> int:
		return 0

class PawnChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'P'

	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int) -> List:
		possibleMoves = []

		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		# Move forward
		moveDirection = [0, 1]
		if teamIndex == 0:
			moveDirection[1] *= -1
		
		moveDistance = 2 if self.getRank(board, cellCoordinates, teamIndex) == 2 else 1

		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
		possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex), rayCells))
		
		# Attack forward left
		moveDirection[0] = -1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleMoves += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		# Attack forward right
		moveDirection[0] = 1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleMoves += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		return possibleMoves
	
	def getRank(self, board: Board, cellCoordinates: List, teamIndex: int) -> int:
		return board.cellHeight - cellCoordinates[1] if teamIndex == 0 else cellCoordinates[1] + 1

class RookChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'R'
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		return possibleMoves

class KnightChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'N'
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

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

		possibleMoves = list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, teamIndex), possibleMoves))

		return possibleMoves

class BishopChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'B'
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		return possibleMoves

class QueenChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'Q'
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		return possibleMoves

class KingChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'K'

	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

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
			possibleMoves += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, teamIndex), rayCells))

		return possibleMoves

class ChessPieceSet(PieceSet):
	def __init__(self):
		super().__init__()

		self.pieces = [
			PawnChessPiece(),
			RookChessPiece(),
			KnightChessPiece(),
			BishopChessPiece(),
			QueenChessPiece(),
			KingChessPiece()
		]

		self.KingPieceType = len(self.pieces) - 1 # NOTE: Assumes King was added last.

	def getPieceTypeFromCharacter(self, character: str) -> int:
		upperCharacter = character.upper()

		for pieceIndex in range(len(self.pieces)):
			piece = self.pieces[pieceIndex]
			if piece.character == upperCharacter:
				return pieceIndex
		
		return -1

	def getTeamIndexFromCharacter(self, character: str) -> int:
		if character.lower() == character:
			return 1
		
		return 0
	