import pygame, random

class Block:
    def __init__(self, xCoord, yCoord, width, height, color, special):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = width
        self.height = height
        self.color = color
        self.special = special
        self.isVisible = True
        self.topRight = (self.xCoord + self.width, self.yCoord)
        self.bottomRight = (self.xCoord + self.width, self.yCoord + self.height)
        self.topLeft = (self.xCoord, self.yCoord)
        self.bottomLeft = (self.xCoord, self.yCoord + self.height)

    def getXCoord(self):
        return self.xCoord

    def getYCoord(self):
        return self.yCoord

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def checkVisible(self):
        return self.isVisible

    def getColor(self):
        return self.color

    def isHit(self, xCoordBall, yCoordBall):
        if (xCoordBall >= self.xCoord and xCoordBall <= self.xCoord + self.width) and (yCoordBall >= self.yCoord and yCoordBall <= self.yCoord + self.height) and self.isVisible:
            self.isVisible = False
            return True
        return False

    def getSpecial(self):
        return self.special


