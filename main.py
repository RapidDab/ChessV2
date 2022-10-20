import os as os
from tabnanny import check 
import pygame as py
py.init()
class Pieces:
    def __init__(self):
        self.imageSize = (100, 100)
        self.gameCor = []
        self.lengameCor = len(self.gameCor)
        self.player1Images = []
        self.player2Images = []
        self.player1 = []
        self.player2 = []
        self.gameRect = []
        self.drawnPiece = []
        self.rect = []
        self.pieces = "rnbqkbnrp"
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRr
        self.fenString = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"

    def loadImages(self):
        os.chdir("C:\ChessV2\Player1")
        for i in os.listdir("C:\ChessV2\Player1"):
            self.player1Images.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))
        os.chdir("C:\ChessV2\Player2")
        for i in os.listdir("C:\ChessV2\Player2"):
            self.player2Images.append(py.transform.scale(py.image.load(i).convert_alpha(), self.imageSize))

    def getImageFile(self, char: str) -> py.Rect:
        file = ""
        if char.islower():
            os.chdir("C:\ChessV2\Player1")
            file = self.player1Images[os.listdir("C:\ChessV2\Player1").index(char + ".png")]
        elif char.isupper():
            os.chdir("C:\ChessV2\Player2")
            file = self.player2Images[os.listdir("C:\ChessV2\Player2").index(char + ".png")]
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
                if i.islower():
                    self.player1.append([i, x, y])
                else:
                    self.player2.append([i, x, y])
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
        #self.p = "rnbqkbnrp"
        self.masterList = [self.r, self.n, self.b, self.q, self.k, self.b, self.n, self.r, self.p]
        self.moves = [[0, 100], [0, -100], [100, 0], [-100, 0], [100, 100], [-100, 100], [100, -100], [-100, -100]]
        self.piecesToMove = ""
    def checkWhichPlayer(self) -> list:
        playerlist = self.player1 if self.piecesToMove.islower() else self.player2
        return playerlist
    def makeMove(self, moves, currentPlayercor):
        x = moves[0]+ currentPlayercor[0]
        y = moves[1] + currentPlayercor[1]
        return [x, y] 
    def getCurrentPieceLegalMoves(self, pieceToMove):
        index = None
        if pieceToMove.isupper():
            index = self.pieces.index(pieceToMove.lower())
        else:
            index = self.pieces.index(pieceToMove)
        return self.masterList[index]
    def checkCurrentPlayer(self, currentLegalMove, currentCor):
        state = True
        playerlist = self.checkWhichPlayer()
        playerx, playery = currentCor[0], currentCor[1]
        for playerInfo in playerlist:
            if playerInfo[0] != currentCor[0] and playerInfo[1] !=currentCor[1]:
                piecex, piecey = playerInfo[1], playerInfo[2]
                if currentLegalMove == [piecex, piecey]:
                    state = False
        return state
            
    def checkBoundares(self, move, cor):
        x = cor[0] + move[0]
        y = cor[1] + move[1]
        if x < 0:
            x = cor[0]
        if y < 0:
            y = cor[1]
        if x > 700:
            x = cor[0]
        if y > 700:
            y = cor[1]
        return [x, y]
    def legalMoves(self, cor):
        x = cor[0]
        y = cor[1]
        if self.piecesToMove.islower():
            if self.piecesToMove == "k":
                for move in self.moves:
                    if self.checkCurrentPlayer(self.checkBoundares(move, cor), cor):
                        self.k.append([x + move[0], y+move[1]])
            print(self.gameCor)

        print("Legalmove move: " + str(self.k))      
    def eraseLegalMoves(self):
        for pieceLegalMoves in self.masterList:
            if pieceLegalMoves != []:
                self.masterList[self.masterList.index(pieceLegalMoves)].clear()
class UI(GameLogic):
    def __init__(self):
        super().__init__()
        self.size = 100
    def drawAlphaRect(self, color, cor, alpha):
        s = py.Surface((self.size, self.size))
        s.set_alpha(alpha)
        s.fill(color)
        screen.blit(s, cor)
    def drawLegalMoves(self, legalPieceMove):
        color = (255,255,0)
        if clicked == True:
            for i in legalPieceMove:
                if i != [None, None]:
                    self.drawAlphaRect((255, 255, 255), (i[0], i[1]), 200)
            x, y = round(startX-50, -2), round(starty-50, -2)
            self.drawAlphaRect((240, 29, 0), (x, y), 255)
            # py.draw.rect(screen, (255, 0, 0), py.Rect(round(startX-50, -2), round(starty-50, -2), 100, 100))

# Loading screen variable and the bacground image
screen = py.display.set_mode((800, 800))
bg = py.image.load("unnamed.jpg").convert()
bg = py.transform.scale(bg, (800, 800))

# Pieces methods needed to initialize
chess = UI()
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
                        # chess.drawLegalMoves()
                        chess.legalMoves([chess.gameCor[movePiece][1], chess.gameCor[movePiece][2]])
                        
        elif event.type == py.MOUSEMOTION:
            if clicked:
                mouse_x, mouse_y = event.pos
                chess.gameCor[movePiece][1] = mouse_x - chess.imageSize[0] / 2
                chess.gameCor[movePiece][2] = mouse_y - chess.imageSize[1] / 2
                chess.rect[movePiece].x = mouse_x - chess.imageSize[0] / 2
                chess.rect[movePiece].y = mouse_x - chess.imageSize[1] / 2
        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False
                end_x, end_y = event.pos
                try:
                    # print(chess.k, [round(end_x-50, -2), round(end_y-50, -2)])
                    if [round(end_x-50, -2), round(end_y-50, -2)] in chess.getCurrentPieceLegalMoves(chess.piecesToMove):
                        chess.gameCor[movePiece][1] = round(end_x - 50, -2)
                        chess.gameCor[movePiece][2] = round(end_y - 50, -2)
                        chess.rect[movePiece].x = round(end_x - 50, -2)
                        chess.rect[movePiece].y = round(end_y - 50, -2)
                    else:
                        chess.gameCor[movePiece][1] = round(startX - 50, -2)
                        chess.gameCor[movePiece][2] = round(starty - 50, -2)
                        chess.rect[movePiece].x = round(startX - 50, -2)
                        chess.rect[movePiece].y = round(starty - 50, -2)
                except:
                    pass
                chess.eraseLegalMoves()
                movePiece = None
    screen.blit(bg, (0, 0))
    chess.drawLegalMoves(chess.getCurrentPieceLegalMoves(chess.piecesToMove))
    chess.drawPieces()
    py.display.flip()
py.quit()
