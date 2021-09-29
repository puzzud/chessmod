from chess.chessGameModel import ChessGameModel
from gui.guiGameView import GuiGameView
from gui.guiGameController import GuiGameController

def main() -> None:
	gameModel = ChessGameModel()
	
	guiGameView = GuiGameView(gameModel)
	guiGameController = GuiGameController(gameModel, guiGameView)

	gameModel.initialize()
	guiGameController.loop()
	gameModel.shutdown()

main()
