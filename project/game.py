from os import sys

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

if __name__ == "__main__":
	profile = False

	for arg in sys.argv[1:]:
		argString: str = arg
		if argString.lower() == "profile":
			profile = True

	if profile:
		import cProfile

		cProfileOutputFilename = "cProfileOutput.dat"
		cProfile.run("main()", cProfileOutputFilename)

		import pstats
		from pstats import SortKey

		with open("cProfileOutputTime.txt", "w") as file:
			p = pstats.Stats(cProfileOutputFilename, stream = file)
			p.sort_stats("time").print_stats()
		
		with open("cProfileOutputCalls.txt", "w") as file:
			p = pstats.Stats(cProfileOutputFilename, stream = file)
			p.sort_stats("calls").print_stats()
	else:
		main()
