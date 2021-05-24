import pygame, random
from block import Block

class BlockRows:
    def __init__(self, rows, cols, blockWidth, blockHeight):
        self.rows = rows
        self.cols = cols
        self.numBlocks = rows*cols
        allBlocks = []
        self.bombBlockNum = 0
        self.livesBlockNum = 0
        pygame.mixer.init()
        self.explosion = pygame.mixer.Sound("sounds\explosion.wav")
        self.life = pygame.mixer.Sound("sounds\life.wav")
        for i in range(rows):
            blockRow = []
            bombBlockNum = 0
            for j in range(cols):
                special = None
                if random.randrange(0, self.numBlocks + 1) % 4 == 0 and bombBlockNum != 1:
                    special = "bomb"
                    self.bombBlockNum += 1
                    bombBlockNum += 1
                elif random.randrange(0, 100) in range(0, 5) and self.livesBlockNum != 1:
                    special = "life"
                    self.livesBlockNum += 1
                else:
                    special = None
                blockRow.append(Block(j+(j*blockWidth), i+(i*blockHeight), blockWidth, blockHeight, (random.randint(5,255), random.randint(5,255), random.randint(5,255)), special))
            allBlocks.append(blockRow)
        self.blocks = allBlocks


    def getRows(self):
        return self.rows

    def getCols(self):
        return self.cols

    def getNumBlocks(self):
        return self.numBlocks

    def isEmpty(self):
        return self.numBlocks == 0

    def getBlocks(self):
        return self.blocks

    def isHitSide(self, ball, xCoordBlock, yCoordBlock, w, h):
        xBall, yBall, wBall, hBall = ball.x, ball.y, ball.width, ball.height
        bLeft = xBall + hBall
        bRight = xBall + hBall + wBall
        tLeft = xBall
        tRight = xBall + wBall

        if xCoordBlock + h - 1 >= bRight >= xCoordBlock + 1:
            print("LEFT SIDE bottomRight")
            return True
        elif xCoordBlock + h - 1 >= tRight >= xCoordBlock + 1:
            print("LEFT SIDE topRight")
            return True
        elif xCoordBlock + w + h - 1>= bLeft >= xCoordBlock + w + 1:
            print("RIGHT SIDE bottomLeft")
            return True
        elif xCoordBlock + w + h - 1 >= tLeft >= xCoordBlock + w + 1:
            print("RIGHT SIDE topLeft")
            return True
        else:
            return False


    def checkHit(self, xCoord, yCoord, ball):
        side = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.blocks[i][j].isHit(xCoord, yCoord):
                    side = self.isHitSide(ball, 
                                          self.blocks[i][j].getXCoord(), self.blocks[i][j].getYCoord(), self.blocks[i][j].getWidth(),
                                          self.blocks[i][j].getHeight())
                    if self.blocks[i][j].getSpecial() == "bomb":
                        if i != 0:
                            self.blocks[i-1][j].isVisible = False
                        if i != self.rows-1:
                            self.blocks[i+1][j].isVisible = False
                        if j != 0:
                            self.blocks[i][j-1].isVisible = False
                        if j != self.cols-1:
                            self.blocks[i][j+1].isVisible = False
                        print("Bomb Block hit")
                        self.explosion.play()
                    elif self.blocks[i][j].getSpecial() == "life":
                        print("Life Block hit")
                        self.life.play()
                        return True, True, side
                    return True, False, side
        return False, False, side

    def __str___(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.blocks[i][j],end = "")
            print()

        

