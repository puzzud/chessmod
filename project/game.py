from gameLogic import GameLogic
from gameRenderer import GameRenderer
from gameController import GameController

def main() -> None:
	gameLogic = GameLogic()
	gameRenderer = GameRenderer(gameLogic)
	gameController = GameController(gameLogic, gameRenderer)

	gameLogic.initialize()
	gameController.loop()
	gameLogic.shutdown()

main()
