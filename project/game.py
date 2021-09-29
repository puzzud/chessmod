from chess.chessGameModel import ChessGameModel
from gui.guiGameView import GuiGameView
from gui.guiGameController import GuiGameController
from cl.clGameView import ClGameView

def main() -> None:
	gameModel = ChessGameModel()
	
	guiGameView = GuiGameView(gameModel)
	guiGameController = GuiGameController(gameModel, guiGameView)

	clGameView = ClGameView(gameModel)

	gameModel.initialize()
	guiGameController.loop()
	gameModel.shutdown()

main()
