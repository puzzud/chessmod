from typing import Dict, List

from board import Board

class Piece:
	def __init__(self):
		self.character = ""
	
	def getPossibleMoves(self, board: Board, cellIndex: int, teamIndex: int):
		return []
	