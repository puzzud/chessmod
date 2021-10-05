from typing import Dict, List

from chess.piece import Piece
from chess.board import Board

class PieceSet():
	def __init__(self):
		self.pieceTypes: list[Piece] = []
		self.pieceTypeCharacters: Dict[Piece, str] = {}

	def getTypeIdFromPieceType(self, pieceType: Piece) -> int:
		return self.pieceTypes.index(pieceType)

	def addPieceType(self, pieceType: Piece, character: str) -> None:
		self.pieceTypes.append(pieceType)
		self.pieceTypeCharacters[pieceType] = character

	def getCharacterFromPieceType(self, pieceType: Piece) -> str:
		return self.pieceTypeCharacters[pieceType]

	def createPieceFromCharacter(self, character: str) -> Piece:
		return Piece()
	
	def createPieceFromTypeId(self, typeId: int) -> Piece:
		return Piece()
	