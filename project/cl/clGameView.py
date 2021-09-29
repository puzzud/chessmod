from typing import List

from engine.gameView import GameView
from chess.chessGameModel import ChessGameModel

class ClGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers = {
			"gameInitialized": self.onGameInitialized,
			"turnStarted": self.onTurnStarted,
			"turnEnded" : self.onTurnEnded,
			"pieceActivated": self.onPieceActivated,
			"pieceDeactivated": self.onPieceDeactivated,
			"invalidCellSelected": self.onInvalidCellSelected,
			"pieceMoved": self.onPieceMoved
		}

		self.attach(self.gameModel, "cellSelected")
		self.gameModel.attach(self, "gameInitialized")
		self.gameModel.attach(self, "turnStarted")
		self.gameModel.attach(self, "turnEnded")
		self.gameModel.attach(self, "pieceActivated")
		self.gameModel.attach(self, "pieceDeactivated")
		self.gameModel.attach(self, "invalidCellSelected")
		self.gameModel.attach(self, "pieceMoved")

		self.chessGameModel = chessGameModel
	
	def __del__(self):
		super().__del__()
	
	def draw(self) -> None:
		board = self.chessGameModel.board
		self.drawBoard(board)

	def drawBoard(self, board: Board) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = (y * board.cellWidth) + x

	def onGameInitialized(self, payload: None) -> None:
		pass

	def onTurnStarted(self, payload: None) -> None:
		print("Turn: " + self.chessGameModel.teamNames[self.chessGameModel.currentTurnTeamIndex])

	def onTurnEnded(self, payload: None) -> None:
		pass
	
	def onGameEnded(self, winningTeamIndex: int) -> None:
		print("Game Ended")
		print("Winner: " + self.chessGameModel.teamNames[winningTeamIndex])

	def onPieceActivated(self, cellIndex: int) -> None:
		#piece = self.chessGameModel.board.getPiece(cellIndex)
		#print("Activated Piece")
		pass

	def onPieceDeactivated(self, cellIndex: int) -> None:
		#print("Deactivated Piece")
		pass

	def onInvalidCellSelected(self, cellIndex: int) -> None:
		print("Invalid Selection: " + str(cellIndex))

	def onPieceMoved(self, movePair: List) -> None:
		#print("Moved Piece")
		pass
	