from gameLogic import GameLogic
from gameRenderer import GameRenderer

def main() -> None:
	gameLogic = GameLogic()
	gameRenderer = GameRenderer(gameLogic)

	gameLogic.initialize()
	gameLogic.shutdown()

main()
