from typing import Dict, List

from chess.pieceSet import PieceSet
import chess.piece
import chess.chessPiece

class ChessPieceSet(PieceSet):
	def __init__(self):
		super().__init__()

		self.addPieceType(chess.chessPiece.PawnChessPiece, 'P')
		self.addPieceType(chess.chessPiece.RookChessPiece, 'R')
		self.addPieceType(chess.chessPiece.KnightChessPiece, 'N')
		self.addPieceType(chess.chessPiece.BishopChessPiece, 'B')
		self.addPieceType(chess.chessPiece.QueenChessPiece, 'Q')
		self.addPieceType(chess.chessPiece.KingChessPiece, 'K')

	def createPieceFromCharacter(self, character: str) -> int:
		upperCharacter = character.upper()

		for pieceType in self.pieceTypes:
			pieceCharacter = self.getCharacterFromPieceType(pieceType)
			if pieceCharacter == upperCharacter:
				piece: chess.piece.Piece = pieceType()
				piece.teamIndex = self.getTeamIndexFromCharacter(character)
				return piece
		return None

	def createPieceFromTypeId(self, typeId: int) -> chess.piece.Piece:
		if typeId < 0:
			return None
		
		if typeId >= len(self.pieceTypes):
			return None

		return self.pieceTypes[typeId]()

	def getTeamIndexFromCharacter(self, character: str) -> int:
		if character.lower() == character:
			return 1
		
		return 0
	