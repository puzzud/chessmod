class GameLogic:
	from board import Board
	
	def __init__(self):
		self.board = self.Board(8, 8)
		self.board.loadFromStringRowList(
			[
				"rnbqkbnr",
				"pppppppp",
				"........",
				"........",
				"........",
				"........",
				"PPPPPPPP",
				"RNBQKBNR"
			]
		)
