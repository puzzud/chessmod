from enum import Enum

import copy

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
	
	def __copy__(self):
		gamePlayerCopy = GamePlayer()
		gamePlayerCopy.typeId = self.typeId
		gamePlayerCopy.teamIndex = self.teamIndex
		gamePlayerCopy.name = self.name

	def copy(self):
		return copy.copy(self)
	