from typing import Dict, List
import functools

import chess.piece
import chess.chessBoard

class ChessPiece(chess.piece.Piece):
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

	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board
		return board.getMovePieceActions(activeCellIndex, targetCellIndex)
