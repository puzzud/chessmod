from typing import Dict, List
from enum import Enum

import pygame
from pygame.locals import *

class PieceTypes(Enum):
  NONE = -1
  PAWN = 0
  ROOK = 1
  KNIGHT = 2
  BISHOP = 3
  QUEEN = 4
  KING = 5
  NUMBER_OF_TYPES = 6

PieceTypeLetters = {
  PieceTypes.NONE.value: '.',
  PieceTypes.PAWN.value: 'P',
  PieceTypes.ROOK.value: 'R',
  PieceTypes.KNIGHT.value: 'N',
  PieceTypes.BISHOP.value: 'B',
  PieceTypes.QUEEN.value: 'Q',
  PieceTypes.KING.value: 'K'
}

BoardCellWidth = 8
BoardCellHeight = 8

class Board:
  def __init__(self, cellWidth: int, cellHeight: int):
    self.cellWidth = cellWidth
    self.cellHeight = cellHeight

    numberOfCells = cellWidth * cellHeight

    self.cellPieceTypes = [PieceTypes.NONE.value] * numberOfCells
    self.cellPieceTeams = [-1] * numberOfCells
  
  def setCell(self, x: int, y: int, contents: Dict) -> None:
    cellIndex = (y * self.cellWidth) + x

    self.cellPieceTypes[cellIndex] = contents["pieceType"]
    self.cellPieceTeams[cellIndex] = contents["teamIndex"]
  
  def loadFromStringRowList(self, stringRowList: List) -> None:
    y = 0
    for stringRow in stringRowList:
      x = 0
      for character in stringRow:
        pieceType = PieceTypes.NONE.value
        teamIndex = -1

        if character is not PieceTypeLetters[PieceTypes.NONE.value]:
          
          for keyPieceType in PieceTypeLetters:
            pieceLetter = PieceTypeLetters[keyPieceType]

            if character is pieceLetter:
              teamIndex = 0
            elif character == pieceLetter.lower():
              teamIndex = 1
            
            if teamIndex > -1:
              pieceType = keyPieceType
              break
        
        self.setCell(x, y, {"pieceType": pieceType, "teamIndex": teamIndex})

        x += 1
      
      y += 1

CellPixelWidth = 32
CellPixelHeight = 32

BackgroundColor = (0, 0, 0)

CellColor0 = (192, 192, 192)
CellColor1 = (128, 128, 128)
CellColors = [
  CellColor0,
  CellColor1
]

PieceColor0 = (255, 255, 255)
PieceColor1 = (0, 0, 0)
PieceColors = [
  PieceColor0,
  PieceColor1
]

def renderPieceIconSurfaces(font) -> List:
  pieceIconSurfaces = []

  for teamIndex in range(2):
    teamPieceIconSurfaces = []

    pieceColor = PieceColors[teamIndex]
    for pieceTypeIndex in range(PieceTypes.NUMBER_OF_TYPES.value):
      pieceIconSurface = font.render(PieceTypeLetters[pieceTypeIndex], True, PieceColors[teamIndex])
      teamPieceIconSurfaces.append(pieceIconSurface)
    
    pieceIconSurfaces.append(teamPieceIconSurfaces)

  return pieceIconSurfaces

def drawBoard(screen: pygame.Surface, board: Board) -> None:
  for y in range(0, board.cellHeight):
    for x in range(0, board.cellWidth):
      cellIndex = (y * board.cellWidth) + x
      
      cellColor = None
      if (cellIndex % 2) == (y % 2):
        cellColor = CellColor0
      else:
        cellColor = CellColor1

      pygame.draw.rect(screen, cellColor, pygame.Rect(x * CellPixelWidth, y * CellPixelHeight, CellPixelWidth, CellPixelHeight))

def drawPieces(screen: pygame.Surface, board: Board, pieceIconSurfaces: List) -> None:
  for y in range(0, board.cellHeight):
    for x in range(0, board.cellWidth):
      cellIndex = (y * board.cellWidth) + x

      cellPieceType = board.cellPieceTypes[cellIndex]
      if cellPieceType is not PieceTypes.NONE.value:
        drawPiece(screen, x, y, cellPieceType, board.cellPieceTeams[cellIndex], pieceIconSurfaces)

def drawPiece(screen: pygame.Surface, cellX: int, cellY: int, pieceType: int, teamIndex: int, pieceIconSurfaces: List) -> None:
  pieceIconSurface = pieceIconSurfaces[teamIndex][pieceType]

  cellLeft = cellX * CellPixelWidth
  cellTop = cellY * CellPixelHeight

  screen.blit(pieceIconSurface, (cellLeft, cellTop))

def main() -> None:
  pygame.init()
  pygame.font.init()

  done = False

  screen = pygame.display.set_mode((640, 480))
  font = pygame.font.SysFont("", int(CellPixelWidth * 1.5))

  pieceIconSurfaces = renderPieceIconSurfaces(font)

  board = Board(BoardCellWidth, BoardCellHeight)
  board.loadFromStringRowList(
    [
      "rnbqkbnr",
      "pppppppp",
      "........",
      "........",
      "........",
      "........",
      "PPPPPPPP",
      "RNBQKBNR"
    ]
  )

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
        done = True
    
    screen.fill(BackgroundColor)

    drawBoard(screen, board)
    drawPieces(screen, board, pieceIconSurfaces)
    
    pygame.display.update()
  
  pygame.quit()

main()
