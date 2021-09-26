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

	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []

		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)
		cellCoordinates[1] -= 1

		possibleMoves.append(board.getCellIndexFromCoordinates(cellCoordinates))

		return possibleMoves

class RookChessPiece(Piece):
	def __init__(self):
		super().__init__()

		self.character = 'R'
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		possibleMoves = []
		possibleMoves.append(0)
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
	