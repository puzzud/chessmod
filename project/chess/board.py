from typing import Dict, List
from enum import Enum

from chess.piece import Piece
from chess.pieceSet import PieceSet

class BoardPieceActionType(Enum):
	REMOVE_FROM_CELL = 0,
	ADD_TO_CELL = 1,
	MOVE_TO_CELL = 2

class Board:
	def __init__(self, cellWidth: int, cellHeight: int, pieceSet):
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight

		numberOfCells = self.getNumberOfCells()
		self.cellContents: list[list[Piece]] = [[]] * numberOfCells

		self.pieceSet: PieceSet = pieceSet

	def getNumberOfCells(self) -> int:
		return self.cellWidth * self.cellHeight

	def getCellCoordinatesFromIndex(self, cellIndex: int) -> List[int]:
		return [
			int(cellIndex % self.cellWidth),
			int(cellIndex / self.cellHeight)
		]

	def getCellIndexFromCoordinates(self, cellCoordinates: List[int]) -> int:
		if cellCoordinates[0] >= self.cellWidth:
			return -1

		if cellCoordinates[1] >= self.cellHeight:
			return -1

		return (cellCoordinates[1] * self.cellWidth) + cellCoordinates[0]

	def areCellCoordinatesOnBoard(self, cellCoordinates: List[int]) -> bool:
		if (cellCoordinates[0] < 0) or (cellCoordinates[0] >= self.cellWidth):
			return False
		
		if (cellCoordinates[1] < 0) or (cellCoordinates[1] >= self.cellHeight):
			return False
		
		return True

	def getCellContents(self, cellIndex: int):
		return self.cellContents[cellIndex]
	
	def setCellContents(self, cellIndex: int, cellContents: List) -> None:
		self.cellContents[cellIndex] = cellContents

	def clearCellContents(self, cellIndex: int) -> None:
		self.cellContents[cellIndex].clear()

	#def addPieceToCell(self, cellIndex: int, piece) -> None:
	#	self.cellContents[cellIndex].append(piece)

	# NOTE: This method assumes only one piece can be in cell.
	def getPieceFromCell(self, cellIndex: int):
		if self.isCellEmpty(cellIndex):
			return None
		
		piece: Piece = self.getCellContents(cellIndex)[0]
		return piece

	def isCellEmpty(self, cellIndex: int) -> bool:
		return len(self.getCellContents(cellIndex)) == 0

	def doesCellHaveOpponentPiece(self, cellIndex: int, teamIndex: int) -> bool:
		if not self.isCellEmpty(cellIndex):
			for _piece in self.getCellContents(cellIndex):
				piece: Piece = _piece
				if piece.teamIndex != teamIndex:
					return True
		
		return False

	def createCellContentsFromCharacter(self, character: str):
		cellContents: list[Piece] = []
		
		if character is '.':
			return cellContents
		
		cellContents.append(self.pieceSet.createPieceFromCharacter(character))
		return cellContents

	def loadFromStringRowList(self, stringRowList: List[str]) -> None:
		y = 0
		for stringRow in stringRowList:
			x = 0
			for character in stringRow:
				cellIndex = self.getCellIndexFromCoordinates([x, y])
				self.setCellContents(cellIndex, self.createCellContentsFromCharacter(character))
				x += 1
			y += 1
	
	def getCellsFromRay(self, sourceCellCoordinates: List[int], direction: List[int], distance: int) -> List[int]:
		cellIndices: list[int] = []
		
		cellCoordinates = sourceCellCoordinates.copy()

		for offset in range(distance):
			cellCoordinates[0] += direction[0]
			cellCoordinates[1] += direction[1]
			if not self.areCellCoordinatesOnBoard(cellCoordinates):
				break

			cellIndex = self.getCellIndexFromCoordinates(cellCoordinates)

			cellIndices.append(cellIndex)

			# Stop after meeting a piece.
			if not self.isCellEmpty(cellIndex):
				break
		
		return cellIndices

	def getValidMoveCellIndices(self, cellIndex: int) -> List[int]:
		piece = self.getPieceFromCell(cellIndex)
		teamIndex = piece.teamIndex
		return piece.getPossibleMoves(self, cellIndex, teamIndex)

	def isValidMoveDestination(self, sourceCellIndex: int, toCellIndex: int) -> bool:
		return toCellIndex in self.getValidMoveCellIndices(sourceCellIndex)

	def reversePieceActions(self, pieceActions: List[dict]) -> List[dict]:
		pieceActions.reverse()
		for pieceAction in pieceActions:
			pieceActionType: int = pieceAction["type"]
			if pieceActionType == BoardPieceActionType.REMOVE_FROM_CELL:
				pieceAction["type"] = BoardPieceActionType.ADD_TO_CELL
			elif pieceActionType == BoardPieceActionType.ADD_TO_CELL:
				pieceAction["type"] = BoardPieceActionType.REMOVE_FROM_CELL
			elif pieceActionType == BoardPieceActionType.MOVE_TO_CELL:
				fromCellIndex: int = pieceAction["fromCellIndex"]
				toCellIndex: int = pieceAction["toCellIndex"]
				pieceAction["toCellIndex"] = fromCellIndex
				pieceAction["fromCellIndex"] = toCellIndex

		return pieceActions

	def executePieceActions(self, pieceActions: List[dict]) -> int:
		for pieceAction in pieceActions:
			pieceActionType: int = pieceAction["type"]
			if pieceActionType == BoardPieceActionType.ADD_TO_CELL:
				cellIndex: int = pieceAction["cellIndex"]
				pieceTypeId = pieceAction["pieceTypeId"]
				if pieceTypeId > -1:
					piece = self.pieceSet.createPieceFromTypeId(pieceTypeId)
					piece.teamIndex = pieceAction["teamIndex"]
					self.setCellContents(cellIndex, [piece])
			elif pieceActionType == BoardPieceActionType.REMOVE_FROM_CELL:
				cellIndex: int = pieceAction["cellIndex"]
				self.clearCellContents(cellIndex)
			elif pieceActionType == BoardPieceActionType.MOVE_TO_CELL:
				fromCellIndex: int = pieceAction["fromCellIndex"]
				toCellIndex: int = pieceAction["toCellIndex"]
				self.clearCellContents(fromCellIndex)
				pieceTypeId = pieceAction["pieceTypeId"]
				if pieceTypeId > -1:
					piece = self.pieceSet.createPieceFromTypeId(pieceTypeId)
					piece.teamIndex = pieceAction["teamIndex"]
					self.setCellContents(toCellIndex, [piece])
			else:
				print("Board::executePieceActions - Encountered unhandled BoardPieceActionType: " + str(pieceActionType))
		
		return 0

	def getPieceActionsFromMove(self, fromCellIndex: int, toCellIndex: int) -> List[dict]:
		fromPiece = self.getPieceFromCell(fromCellIndex)
		toPiece = self.getPieceFromCell(toCellIndex)

		return [
			{
				"type": BoardPieceActionType.REMOVE_FROM_CELL,
				"cellIndex": toCellIndex,
				"pieceTypeId": -1 if toPiece is None else self.pieceSet.getTypeIdFromPieceType(type(toPiece)),
				"teamIndex": -1 if toPiece is None else toPiece.teamIndex
			},
			{
				"type": BoardPieceActionType.MOVE_TO_CELL,
				"fromCellIndex": fromCellIndex,
				"toCellIndex": toCellIndex,
				"pieceTypeId": -1 if fromPiece is None else self.pieceSet.getTypeIdFromPieceType(type(fromPiece)),
				"teamIndex": -1 if fromPiece is None else fromPiece.teamIndex
			}
		]

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> List[dict]:
		pieceActions = self.getPieceActionsFromMove(fromCellIndex, toCellIndex)
	
		self.executePieceActions(pieceActions)

		return pieceActions
