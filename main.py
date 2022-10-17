import os

import pygame
import pygame as py
import json

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
        self.fenString = "nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRr"

    def loadImages(self):
        os.chdir("C:\ChessV2\Player1")
        for i in os.listdir("C:\ChessV2\Player1"):
            self.player1.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))
        os.chdir("C:\ChessV2\Player2")
        for i in os.listdir("C:\ChessV2\Player2"):
            self.player2.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))

    def getImageFile(self, char: str) -> pygame.Rect:
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
                self.gameCor.append([x, y])
                x += 100

    def drawPieces(self):
        for i, num in enumerate(self.gameCor):
            screen.blit(self.gameRect[i], (num[0], num[1]))

    def makeRect(self):
        for i in self.gameCor:
            self.rect.append(pygame.Rect((i[0], i[1]), (98, 98)))
    # def getCor(self, index):


# Loading screen variable and the bacground image
screen = py.display.set_mode((800, 800))
bg = py.image.load("unnamed.jpg").convert()
bg = py.transform.scale(bg, (800, 800))

# Pieces methods needed to initialize
pieces = Pieces()
pieces.loadImages()
pieces.fenParse()
pieces.makeRect()

# Game loop variables
loop = True
clicked = False
movePiece = ""

while loop:
    for event in py.event.get():
        if event.type == py.QUIT:
            loop = False
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                for i in pieces.rect:
                    if i.collidepoint(event.pos):
                        movePiece = pieces.rect.index(i)
                        startX, starty = event.pos
                        print(i)
                        clicked = True
        elif event.type == py.MOUSEMOTION:
            if clicked:
                mouse_x, mouse_y = event.pos
                pieces.gameCor[movePiece][0] = mouse_x - pieces.imageSize[0] / 2
                pieces.gameCor[movePiece][1] = mouse_y - pieces.imageSize[1] / 2
        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False
                end_x, end_y = event.pos
                pieces.gameCor[movePiece][0] = round(end_x - 50, -2)
                pieces.gameCor[movePiece][1] = round(end_y - 50, -2)
    screen.blit(bg, (0, 0))
    pieces.drawPieces()
    py.display.flip()
py.quit()
