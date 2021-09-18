from gameLogic import GameLogic
from gameRenderer import GameRenderer

def main() -> None:
	gameLogic = GameLogic()
	gameRenderer = GameRenderer(gameLogic)

	while not gameLogic.done:
		gameLogic.proccessEvents()
		gameRenderer.draw()
	
	gameLogic.shutdown()

main()
