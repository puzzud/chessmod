from typing import Dict, List

from chess.pieceSet import PieceSet
import chess.piece
#import chess.chessPiece
import chess.pawnChessPiece
import chess.rookChessPiece
import chess.knightChessPiece
import chess.bishopChessPiece
import chess.queenChessPiece
import chess.kingChessPiece

class ChessPieceSet(PieceSet):
	def __init__(self):
		super().__init__()

		self.addPieceType(chess.pawnChessPiece.PawnChessPiece, 'P')
		self.addPieceType(chess.rookChessPiece.RookChessPiece, 'R')
		self.addPieceType(chess.knightChessPiece.KnightChessPiece, 'N')
		self.addPieceType(chess.bishopChessPiece.BishopChessPiece, 'B')
		self.addPieceType(chess.queenChessPiece.QueenChessPiece, 'Q')
		self.addPieceType(chess.kingChessPiece.KingChessPiece, 'K')

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
	
	def getCharacterFromPiece(self, piece: chess.piece.Piece) -> str:
		character = super().getCharacterFromPiece(piece)

		if piece.teamIndex == 1:
			return character.lower()
	
		return character
	