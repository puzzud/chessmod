from typing import Dict, List

from piece import Piece
from board import Board

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
		return possibleMoves

class KnightChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'N'

class BishopChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'B'

class QueenChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'Q'

class KingChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'K'

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
	