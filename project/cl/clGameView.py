from typing import Any, Dict, List

from engine.gameView import GameView
from engine.gamePlayer import GamePlayer

from chess.chessGameModel import ChessGameModel
from chess.chessBoard import ChessBoard

class ClGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers["gameInitialized"] = self.onGameInitialized
		self.signalHandlers["gameEnded"] = self.onGameEnded
		self.signalHandlers["turnStarted"] = self.onTurnStarted
		self.signalHandlers["turnEnded"] = self.onTurnEnded
		self.signalHandlers["pieceActivated"] = self.onPieceActivated
		self.signalHandlers["pieceDeactivated"] = self.onPieceDeactivated
		self.signalHandlers["invalidCellSelected"] = self.onInvalidCellSelected
		self.signalHandlers["actionsMade"] = self.onActionsMade

		self.attach(chessGameModel, "cellSelected")

		chessGameModel.attach(self, "gameInitialized")
		chessGameModel.attach(self, "gameEnded")
		chessGameModel.attach(self, "turnStarted")
		chessGameModel.attach(self, "turnEnded")
		chessGameModel.attach(self, "pieceActivated")
		chessGameModel.attach(self, "pieceDeactivated")
		chessGameModel.attach(self, "invalidCellSelected")
		chessGameModel.attach(self, "actionsMade")
	
		self.board: ChessBoard = None
		self.teamNames: list[str] = []

	def __del__(self):
		super().__del__()
	
	def draw(self) -> None:
		self.drawBoard(self.board)

	def drawBoard(self, board: ChessBoard) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = board.getCellIndexFromCoordinates([x, y])

	def onGameInitialized(self, payload: Dict[str, Any]) -> None:
		self.board = ChessBoard()
		self.board.loadFromStringRowList(payload["boardStringRowList"])

		self.teamNames = payload["teamNames"].copy()

	def onPlayerAdded(self, player: GamePlayer) -> None:
		print("Player Added: " + player.name)

	def onPlayerTypeUpdated(self, payload: Dict[str, Any]) -> None:
		print("Player Type Updated: " + str(payload["index"]) + " " + str(payload["value"]))

	def onGameEnded(self, winningTeamIndex: int) -> None:
		print("Game Ended")
		if winningTeamIndex > -1:
			print("Winner: " + self.teamNames[winningTeamIndex])
		else:
			print("Draw")

	def onTurnStarted(self, currentTurnTeamIndex: int) -> None:
		#print("Turn: " + self.chessGameModel.teamNames[self.chessGameModel.currentTurnTeamIndex])
		pass

	def onTurnEnded(self, payload: None) -> None:
		pass

	def onPieceActivated(self, payload: Dict[str, Any]) -> None:
		#piece = self.chessGameModel.board.getPiece(cellIndex)
		#print("Activated Piece")
		pass

	def onPieceDeactivated(self, cellIndex: int) -> None:
		#print("Deactivated Piece")
		pass

	def onInvalidCellSelected(self, cellIndex: int) -> None:
		print("Invalid Selection: " + str(cellIndex))

	def onActionsMade(self, pieceActions: List[dict]) -> None:
		#print("Moved Piece")
		pass
	