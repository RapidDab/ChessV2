import os

import pygame as py
import json
#Hello world
py.init()
class Pieces:
    def __init__(self):
        self.player1 = []
        self.player2 = []
        self.imageSize = (100, 100)
        self.gameCor = []
        self.gameRect = []
        self.drawnPiece = []
        self.rect = []
        self.p = "rnbqkbnrp"
        # nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRr
        self.fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRr"

    def loadImages(self):
        os.chdir("C:\ChessV2\Player1")
        for i in os.listdir("C:\ChessV2\Player1"):
            self.player1.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))
        os.chdir("C:\ChessV2\Player2")
        for i in os.listdir("C:\ChessV2\Player2"):
            self.player2.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))

    def getImageFile(self, char: str) -> py.Rect:
        file = ""
        if char.islower():
            os.chdir("C:\ChessV2\Player1")
            file = self.player1[os.listdir("C:\ChessV2\Player1").index(char + ".png")]
        elif char.isupper():
            os.chdir("C:\ChessV2\Player2")
            file = self.player2[os.listdir("C:\ChessV2\Player2").index(char + ".png")]
        return file

    def fenParse(self):
        x, y = 0, 0
        for i in self.fenString:
            s = self.getImageFile(i) if self.getImageFile(i) != "" else None
            if i.isnumeric():
                x += int(i) * 100
            elif i == "/":
                y += 100
                x = 0
            else:
                self.gameRect.append(s)
                self.gameCor.append([i, x, y])
                x += 100

    def drawPieces(self):
        for i, num in enumerate(self.gameCor):
            screen.blit(self.gameRect[i], (num[1], num[2]))

    def makeRect(self):
        for i in self.gameCor:
            self.rect.append(py.Rect((i[1], i[2]), (98, 98)))
    # def getCor(self, index):
class GameLogic(Pieces):
    def __init__(self):
        super().__init__()
        self.r = []
        self.n = []
        self.b = []
        self.k = []
        self.q = []
        self.p = []
        self.moves = [[0, 100], [0, -100], [100, 100], [-100, 100], [100, -100], [-100, -100]]
        self.piecesToMove = ""
        
    def legalMoves(self):
        cor = [self.gameCor[movePiece][1], self.gameCor[movePiece][2]]
        if self.piecesToMove.islower():
            if self.piecesToMove == "k":
                print(cor)


# Loading screen variable and the bacground image
screen = py.display.set_mode((800, 800))
bg = py.image.load("unnamed.jpg").convert()
bg = py.transform.scale(bg, (800, 800))

# Pieces methods needed to initialize
chess = GameLogic()
chess.loadImages()
chess.fenParse()
chess.makeRect()
# Game loop variables
loop = True
clicked = False
while loop:
    for event in py.event.get():
        if event.type == py.QUIT:
            loop = False
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                for i in chess.rect:
                    if i.collidepoint(event.pos):
                        movePiece = chess.rect.index(i)
                        startX, starty = event.pos
                        clicked = True
                        chess.piecesToMove = chess.gameCor[movePiece][0]
                        chess.legalMoves()
                        
        elif event.type == py.MOUSEMOTION:
            if clicked:
                mouse_x, mouse_y = event.pos
                chess.gameCor[movePiece][1] = mouse_x - chess.imageSize[0] / 2
                chess.gameCor[movePiece][2] = mouse_y - chess.imageSize[1] / 2
        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False
                end_x, end_y = event.pos
                try:
                    chess.gameCor[movePiece][1] = round(end_x - 50, -2)
                    chess.gameCor[movePiece][2] = round(end_y - 50, -2)
                    movePiece = None
                except:
                    pass
    screen.blit(bg, (0, 0))
    chess.drawPieces()
    py.display.flip()
py.quit()
