from os import sys

from chess.chessGameModel import ChessGameModel
from chess.chessGameController import ChessGameController
from chess.guiChessGameView import GuiChessGameView
from chess.clChessGameView import ClChessGameView

def main() -> None:
	gameModel = ChessGameModel()
	
	chessGameController = ChessGameController(gameModel)

	guiChessGameView = GuiChessGameView(gameModel, chessGameController)
	clChessGameView = ClChessGameView(gameModel, chessGameController)

	gameModel.initialize()
	guiChessGameView.loop()
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
