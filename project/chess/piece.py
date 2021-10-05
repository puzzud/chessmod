from typing import Dict, List

from chess.board import Board

class Piece:
	def __init__(self, teamIndex: int = -1):
		self.teamIndex: int = teamIndex

	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int) -> List[int]:
		return []
	