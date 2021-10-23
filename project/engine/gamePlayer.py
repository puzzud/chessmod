from enum import Enum

class GamePlayerTypeId(Enum):
	AI = -1
	NONE = 0
	LOCAL = 1
	REMOTE = 2

class GamePlayer():
	def __init__(self):
		self.typeId = GamePlayerTypeId.NONE
		self.teamIndex = -1
		self.name = ""
	