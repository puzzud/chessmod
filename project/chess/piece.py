from typing import Dict, List

class Piece:
	def __init__(self, teamIndex: int = -1):
		self.teamIndex: int = teamIndex

	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		return []
	