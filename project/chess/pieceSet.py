from typing import Dict, List

from chess.piece import Piece
from chess.board import Board

class PieceSet():
	def __init__(self):
		self.pieces = []
	
	def getPieceFromType(self, pieceType: int) -> Piece:
		return self.pieces[pieceType]

	def getTypeFromPieceClass(self, pieceClass: Piece) -> int:
		for pieceIndex in range(len(self.pieces)):
			currentPiece = self.pieces[pieceIndex]
			currentPieceType = type(currentPiece)
			if currentPieceType is pieceClass:
				return pieceIndex
		
		return -1

	def getPiecePropertiesFromCharacter(self, character: str) -> Dict:
		return {
			"pieceType": self.getPieceTypeFromCharacter(character),
			"teamIndex": self.getTeamIndexFromCharacter(character)
		}
	
	def getPieceTypeFromCharacter(self, character: str) -> int:
		return -1

	def getTeamIndexFromCharacter(self, character: str) -> int:
		return 0
