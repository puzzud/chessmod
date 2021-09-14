from enum import Enum

class PieceTypes(Enum):
	NONE = -1
	PAWN = 0
	ROOK = 1
	KNIGHT = 2
	BISHOP = 3
	QUEEN = 4
	KING = 5
	NUMBER_OF_TYPES = 6

PieceTypeLetters = {
	PieceTypes.NONE.value: '.',
	PieceTypes.PAWN.value: 'P',
	PieceTypes.ROOK.value: 'R',
	PieceTypes.KNIGHT.value: 'N',
	PieceTypes.BISHOP.value: 'B',
	PieceTypes.QUEEN.value: 'Q',
	PieceTypes.KING.value: 'K'
}
