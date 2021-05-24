#Sam G., Jimmy C., Lucas F.

import pygame, random
from BlockRows import BlockRows
from Levels import Levels
import sys
import time

heartImage = pygame.image.load("images/heart.png")
bethImage = pygame.image.load("images/beth.png")
jerryImage = pygame.image.load("images/jerry.png")
rickImage = pygame.image.load("images/rickpointing.png")

class Breakout:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.menuSound = pygame.mixer.Sound("sounds\menu-navigate-02.wav")
        self.menuSound2 = pygame.mixer.Sound("sounds\menu-navigate-01.wav")
        self.menuSound3 = pygame.mixer.Sound("sounds\menu-navigate-00.wav")
        self.hitSound = pygame.mixer.Sound("sounds\hit-01.wav")
        self.winSound = pygame.mixer.Sound("sounds\win.wav")
        self.explosionSound = pygame.mixer.Sound("sounds\explosion.wav")
        self.loseSound = pygame.mixer.Sound("sounds\lose.wav")
        self.levels = Levels()
        self.movingRight, self.movingDown = True, True
        self.size = self.width, self.height = 250, 300
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_icon(pygame.image.load("images/morty.png"))
        pygame.display.set_caption("Breakout")
        self.paddleWidth, self.paddleHeight = 55, 5
        self.xCoordBall, self.yCoordBall = random.randrange(0, self.width), random.randrange(120, self.height - 80)
        self.xCoordPaddle, self.yCoordPaddle = self.xCoordBall - (self.paddleWidth / 2), self.height - self.paddleHeight - 15
        self.xSpeed, self.ySpeed = 2, random.choice([-3, 3])
        self.font = pygame.font.SysFont("Terminal", 14)
        self.lives = 3
        self.level = 1
        self.levelInfo = self.getLevel()
        self.points = self.levelInfo[2]
        #self.timeGone = None
        self.draw()
        #self.seconds = self.levelInfo[3]
        self.blocks = BlockRows(self.levelInfo[0], self.levelInfo[1], 24, 10)
        #print(str(self.xCoordBall)+" "+str(self.yCoordBall))
        self.white = (255, 255, 255)
        self.black = (0, 0, 0) 
        self.red = (255, 0, 0)
        self.stillPlaying = True
        self.playAgain = False
        self.numBlocks = self.blocks.isEmpty()
        self.score = 0
        self.pointtime = 0

    def getLevel(self):
        levels = {
            1: self.levels.one,
            2: self.levels.two,
            3: self.levels.three,
            4: self.levels.four,
            5: self.levels.fiveUp
            }
        if self.level > 5:
            func = levels.get(5)
        else:
            func = levels.get(self.level)
        return func()

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.xCoordPaddle, self.yCoordPaddle, self.paddleWidth, self.paddleHeight), 0)
        self.ball = pygame.draw.circle(self.screen, (255, 255, 255), (self.xCoordBall, self.yCoordBall), 4, 0)
        pointsText = self.font.render("Points: " + str(self.points), True, (255, 255, 255))
        livesText = self.font.render("Lives: " + str(self.lives), True, (255, 255, 255))
        #if self.timeGone:
         #   timeLeft = self.font.render("Time Left: " + str(round(self.seconds - self.timeGone, 2)), True, (255, 255, 255))
          #  self.screen.blit(timeLeft, [150, self.height - 10])        
        self.screen.blit(pointsText, [25, self.height - 10])
        self.screen.blit(livesText, [100, self.height - 10])

    def message_to_screen(self, msg, color):
        msg = msg.split("~")
        screen_text = self.font.render(msg[0], True, color)
        playAgain = self.font.render(msg[1], True, color)
        self.screen.blit(screen_text, [(self.width / 4) - 30, self.height/3])
        self.screen.blit(playAgain, [(self.width / 10) + 20, self.height / 2])

    def restart(self, levelUp=False, restartLevel=False, restartGame=False):
        self.movingRight, self.movingDown = True, True
        self.screen = pygame.display.set_mode(self.size)
        self.xCoordBall, self.yCoordBall = random.randrange(0, self.width), random.randrange(120, self.height - 80)
        self.xCoordPaddle, self.yCoordPaddle = self.xCoordBall - (self.paddleWidth / 2), self.height - self.paddleHeight - 15
        self.xSpeed, self.ySpeed = 2, random.choice([-3, 3])
        self.draw()
        if levelUp:
            self.points += self.levelInfo[2]
            self.level += 1
        elif self.restartLevel:
            pass
        elif self.restartGame:
            self.level = 1
            self.mainMenu()
            self.points = self.levelInfo[2]
        self.levelInfo = self.getLevel()
        self.seconds = self.levelInfo[3]
        self.blocks = BlockRows(self.levelInfo[0], self.levelInfo[1], 24, 10)
        #print(str(self.xCoordBall)+" "+str(self.yCoordBall))
        self.stillPlaying = True
        self.playAgain = False
        self.numBlocks = self.blocks.isEmpty()

    def checkHighScore(self, score):
        scoreList = []
        with open('High_Score.txt', 'r') as file:
            for line in file:
                scoreList.append(line)
        #print(scoreList)
        scoreListParsed = []
        for line in scoreList:
            scoreListParsed.append(line.split("\t"))
        #print(scoreListParsed)
        newScoreAdded = False
        for i in range(len(scoreListParsed)):
           if not newScoreAdded and score > int(scoreListParsed[i][2]):
               name = input("What are your initials? (Limit 3): ")
               newHighScore = [str(i+1), str(name), str(score)+"\n"]
               scoreListParsed.insert(i, newHighScore)
               #print(scoreListParsed)
               newScoreAdded = True
           elif newScoreAdded:
               scoreListParsed[i][0] =  str(int(scoreListParsed[i][0])+1)
        highScoreText = """"""
        listLen = 10
        if len(scoreListParsed) < 10:
            listlen = len(scoreListParsed)
        for i in range(listLen):
            for j in range(len(scoreListParsed[i])):
                highScoreText += str(scoreListParsed[i][j])
                if j != len(scoreListParsed[i])-1:
                    highScoreText += "\t"
        delete = open('High_Score.txt', 'r+')
        delete.truncate()
        f = open('High_Score.txt', 'w')
        f.write(highScoreText)
        f.close()
                   
    def mainMenu(self):
        self.lives=3
        started = False
        font2 = pygame.font.SysFont("Terminal", 28)
        selection = 0
        while not started:
            self.screen.fill((random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
            titleLabel = font2.render("BREAKOUT", True, self.black)
            playLabel = self.font.render("Play",True,self.black)
            directionsLabel = self.font.render("Directions",True,self.black)
            scoresLabel = self.font.render("High Scores",True,self.black)
            pressEnter = self.font.render("Press Enter to Select",True,self.black)
            self.screen.blit(titleLabel, [(self.width/2)-55, (self.height/4)])
            self.screen.blit(playLabel, [(self.width/3)-55, (self.height*(3/5))])
            self.screen.blit(directionsLabel, [(self.width*(2/3))-75, (self.height*(3/5))])
            self.screen.blit(scoresLabel, [(self.width)-75, (self.height*(3/5))])
            self.screen.blit(pressEnter, [((self.width)/2)-45, (self.height/4)+50])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #print("Left Arrow Pressed")
                        self.menuSound.play()
                        if selection == 0:
                            selection = 2
                        else:
                            selection -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.menuSound.play()
                        #print("Right Arrow Pressed")
                        if selection == 2:
                            selection = 0
                        else:
                            selection += 1
                    elif event.key == pygame.K_RETURN:
                        self.menuSound2.play()
                        #print("Enter Key Pressed")
                        if selection == 0:
                            return
                        elif selection == 1:
                            reading = True
                            directionsLabel = self.font.render("Directions:",True,self.red)
                            dirLabel1Row1 = self.font.render("The Game Consists Of Five Levels. Each consecutive",True,self.red)
                            dirLabel1Row2 = self.font.render("level consists of one more row of bricks than the",True,self.red)
                            dirLabel1Row3 = self.font.render("previous level.",True,self.red)
                            dirLabel2Row1 = self.font.render("Player gets three lives at the start of the game.",True,self.red)
                            dirLabel3Row1 = self.font.render("The player’s paddle is to be controlled by the",True,self.red)
                            dirLabel3Row2 = self.font.render("arrow pad. (Right arrow to go right, Left",True,self.red)
                            dirLabel3Row3 = self.font.render("arrow to go left)",True,self.red)
                            dirLabel4Row1 = self.font.render("The player must keep the ball from hitting the",True,self.red)
                            dirLabel4Row2 = self.font.render("bottom of the screen.(One life will be lost for",True,self.red)
                            dirLabel4Row3 = self.font.render("every time the player is unable to do so)",True,self.red)
                            dirLabel5Row1 = self.font.render("The score is calculated based on time taken to",True,self.red)
                            dirLabel5Row2 = self.font.render("complete a level and number of bricks that remain",True,self.red)
                            dirLabel5Row3 = self.font.render("(fast time with few bricks destroyed yields a high",True,self.red)
                            dirLabel5Row4 = self.font.render("score)",True,self.red)
                            dirLabel6Row1 = self.font.render("Player who hits a “Bomb Block” shall remove a total",True,self.red)
                            dirLabel6Row2 = self.font.render("of four blocks from the screen while only losing",True,self.red)
                            dirLabel6Row3 = self.font.render("points for the value of one block.",True,self.red)
                            dirLabel7Row1 = self.font.render("The top 10 high scores shall be stored in the",True,self.red)
                            dirLabel7Row2 = self.font.render("“High Score” section of the menu.",True,self.red)
                            while reading:

                                self.screen.fill(self.white)
                                self.screen.blit(directionsLabel,(5,5))
                                self.screen.blit(dirLabel1Row1,(7,15))
                                self.screen.blit(dirLabel1Row2,(7,25))
                                self.screen.blit(dirLabel1Row3,(7,35))
                                self.screen.blit(dirLabel2Row1,(7,45))
                                self.screen.blit(dirLabel3Row1,(7,55))
                                self.screen.blit(dirLabel3Row2,(7,65))
                                self.screen.blit(dirLabel3Row3,(7,75))
                                self.screen.blit(dirLabel4Row1,(7,85))
                                self.screen.blit(dirLabel4Row2,(7,95))
                                self.screen.blit(dirLabel4Row3,(7,105))
                                self.screen.blit(dirLabel5Row1,(7,115))
                                self.screen.blit(dirLabel5Row2,(7,125))
                                self.screen.blit(dirLabel5Row3,(7,135))
                                self.screen.blit(dirLabel5Row4,(7,145))
                                self.screen.blit(dirLabel6Row1,(7,155))
                                self.screen.blit(dirLabel6Row2,(7,165))
                                self.screen.blit(dirLabel6Row3,(7,175))
                                self.screen.blit(dirLabel7Row1,(7,185))
                                self.screen.blit(dirLabel7Row2,(7,195))
                                pygame.display.update()
                                for event2 in pygame.event.get():
                                    if event2.type == pygame.KEYDOWN:
                                        if event2.key == pygame.K_RETURN:
                                            self.menuSound3.play()
                                            reading = False
                                            break
                        else:
                            scoreList = []
                            with open('High_Score.txt', 'r') as file:
                                for line in file:
                                    scoreList.append(line)
                            scoreListParsed = []
                            for line in scoreList:
                                scoreListParsed.append(line.split("\t"))
                            highScoreLabel1 = self.font.render(str(scoreListParsed[0][0])+"     "+str(scoreListParsed[0][1])+"     "+str(scoreListParsed[0][2])[0:len(scoreListParsed[0][2])-1],True,self.red)
                            highScoreLabel2 = self.font.render(str(scoreListParsed[1][0])+"     "+str(scoreListParsed[1][1])+"     "+str(scoreListParsed[1][2])[0:len(scoreListParsed[1][2])-1],True,self.red)
                            highScoreLabel3 = self.font.render(str(scoreListParsed[2][0])+"     "+str(scoreListParsed[2][1])+"     "+str(scoreListParsed[2][2])[0:len(scoreListParsed[2][2])-1],True,self.red)
                            highScoreLabel4 = self.font.render(str(scoreListParsed[3][0])+"     "+str(scoreListParsed[3][1])+"     "+str(scoreListParsed[3][2])[0:len(scoreListParsed[3][2])-1],True,self.red)
                            highScoreLabel5 = self.font.render(str(scoreListParsed[4][0])+"     "+str(scoreListParsed[4][1])+"     "+str(scoreListParsed[4][2])[0:len(scoreListParsed[4][2])-1],True,self.red)
                            highScoreLabel6 = self.font.render(str(scoreListParsed[5][0])+"     "+str(scoreListParsed[5][1])+"     "+str(scoreListParsed[5][2])[0:len(scoreListParsed[5][2])-1],True,self.red)
                            highScoreLabel7 = self.font.render(str(scoreListParsed[6][0])+"     "+str(scoreListParsed[6][1])+"     "+str(scoreListParsed[6][2])[0:len(scoreListParsed[6][2])-1],True,self.red)
                            highScoreLabel8 = self.font.render(str(scoreListParsed[7][0])+"     "+str(scoreListParsed[7][1])+"     "+str(scoreListParsed[7][2])[0:len(scoreListParsed[7][2])-1],True,self.red)
                            highScoreLabel9 = self.font.render(str(scoreListParsed[8][0])+"     "+str(scoreListParsed[8][1])+"     "+str(scoreListParsed[8][2])[0:len(scoreListParsed[8][2])-1],True,self.red)
                            highScoreLabel10 = self.font.render(str(scoreListParsed[9][0])+"     "+str(scoreListParsed[9][1])+"     "+str(scoreListParsed[9][2])[0:len(scoreListParsed[9][2])-1],True,self.red)
                            
                            inHighScore = True
                            while inHighScore:
                                self.screen.fill(self.white)
                                self.screen.blit(highScoreLabel1,(80,10))
                                self.screen.blit(highScoreLabel2,(80,20))
                                self.screen.blit(highScoreLabel3,(80,30))
                                self.screen.blit(highScoreLabel4,(80,40))
                                self.screen.blit(highScoreLabel5,(80,50))
                                self.screen.blit(highScoreLabel6,(80,60))
                                self.screen.blit(highScoreLabel7,(80,70))
                                self.screen.blit(highScoreLabel8,(80,80))
                                self.screen.blit(highScoreLabel9,(80,90))
                                self.screen.blit(highScoreLabel10,(80,100))
                                pygame.display.update()
                                for event2 in pygame.event.get():
                                    if event2.type == pygame.KEYDOWN:
                                        if event2.key == pygame.K_RETURN:
                                            self.menuSound3.play()
                                            inHighScore = False
                                            break

            if selection == 0:
                pygame.draw.rect(self.screen, self.black, ((self.width / 3) - 57, (self.height * (3/5)), 25, 12), 1)
                self.screen.blit(rickImage, ((self.width / 3) - 57, (self.height * (3/5)) + 20))
            elif selection == 1:
                pygame.draw.rect(self.screen, self.black, ((self.width * (2/3)) - 77, (self.height * (3/5)), 50, 12), 1)
                self.screen.blit(rickImage, ((self.width * (2/3)) - 77, (self.height * (3/5)) + 20))
            else:
                pygame.draw.rect(self.screen, self.black, ((self.width) - 77, (self.height * (3/5)), 60, 12), 1)
                self.screen.blit(pygame.transform.flip(rickImage, True, False), ((self.width * (1/2)), (self.height * (3/5)) + 20))

            clock = pygame.time.Clock()
            clock.tick(5)
            pygame.display.flip()

    def checkInputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.xCoordPaddle > 0:
                self.xCoordPaddle -= 5
        elif keys[pygame.K_RIGHT]:   
            if self.xCoordPaddle < pygame.display.get_surface().get_width() - self.paddleWidth:
                self.xCoordPaddle += 5
        elif keys[pygame.K_ESCAPE]:
            sys.exit()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.xCoordPaddle > 0:
                    self.xCoordPaddle -= 5
            elif keys[pygame.K_RIGHT]:   
                if self.xCoordPaddle < pygame.display.get_surface().get_width() - self.paddleWidth:
                    self.xCoordPaddle += 5
            elif keys[pygame.K_ESCAPE]:
                sys.exit()


    def gameOver(self):
        self.loseSound.play()
        self.lives -= 1
        backToMenu = False
        while self.stillPlaying:   
            self.screen.fill(self.white)
            if self.lives == 0:
                self.message_to_screen("Game Over!~You are Out of Lives. Press Escape to Quit.", self.red)
                enterLabel = self.font.render("Or Press Enter to Go Back to the Main Menu.",True,self.red)
                self.screen.blit(enterLabel,((self.width / 10) + 10, self.height / 2 + 30))
                pygame.display.update()
                for i in pygame.event.get():
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_ESCAPE:
                            self.checkHighScore(self.points)
                            sys.exit()
                        if i.key == pygame.K_RETURN:
                            self.checkHighScore(self.points)
                            self.mainMenu()
                            backToMenu = True
                            self.restartGame = True
                            self.restartLevel = True
                            self.stillPlaying = False
                            self.playAgain = True
                            self.levelUp = False
                            self.level = 1
                            self.points = self.levelInfo[2]
                if backToMenu:
                    break
            else:
                self.message_to_screen("Level Failed!~Press P to Continue or Q to Quit.", self.red)
                pygame.display.update()
                for i in pygame.event.get():
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_q:
                            self.checkHighScore(self.points)
                            sys.exit()
                        if i.key == pygame.K_p:
                            self.stillPlaying = False
                            self.playAgain = True
                            self.levelUp = False
                            self.restartLevel = True
                            self.restartGame = False
    
    def LevelUp(self):
        self.winSound.play()
        while self.stillPlaying:   
            self.screen.fill(self.white)
            self.message_to_screen("Level Complete! You Earned {0} Points!~Press P to Continue or Q to Quit.".format(self.points), self.red)
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_q:
                        self.checkHighScore(self.points)
                        sys.exit()
                    if i.key == pygame.K_p:
                        self.stillPlaying = False
                        self.playAgain = True
                        self.levelUp = True
                        self.restartLevel = False
                        self.restartGame = False

    def checkCollisions(self):
        if ((self.yCoordBall >= self.yCoordPaddle and self.yCoordBall <= self.yCoordPaddle + self.paddleHeight) and
            (self.xCoordBall >= self.xCoordPaddle and self.xCoordBall <= self.xCoordPaddle + self.paddleWidth)):
            #PADDLE HIT
            self.hitSound.play()
            rec1 = range(int(self.xCoordPaddle), int(self.xCoordPaddle) + 10)
            rec2 = range(int(self.xCoordPaddle) + 10, int(self.xCoordPaddle) + 20)
            rec3 = range(int(self.xCoordPaddle) + 20, int(self.xCoordPaddle) + 30)
            rec4 = range(int(self.xCoordPaddle) + 30, int(self.xCoordPaddle) + 40)
            rec5 = range(int(self.xCoordPaddle) + 40, int(self.xCoordPaddle) + 50)
            if self.xCoordBall in rec1:
                self.xSpeed = -6 
            elif self.xCoordBall in rec2:
                self.xSpeed = -4
            elif self.xCoordBall in rec3:
                if (self.xCoordBall <= 24 and self.xCoordBall >= 20) or self.xCoordBall == 20 or self.xCoordBall == 24:
                    self.xSpeed = -3
                elif (self.xCoordBall <= 29 and self.xCoordBall >= 25) or self.xCoordBall == 25 or self.xCoordBall == 29:
                    self.xSpeed = 3
                else:
                    self.xSpeed = random.choice([-3, 3])
                self.ySpeed = 3
            elif self.xCoordBall in rec4:
                self.xSpeed = 4
            elif self.xCoordBall in rec5:
                self.xSpeed = 6
            self.ySpeed *= -1
            self.movingDown = not self.movingDown

        checkHit = self.blocks.checkHit(self.xCoordBall, self.yCoordBall, self.ball)
        if checkHit[0]:
            self.hitSound.play()
            if checkHit[1]:
                self.lives += 1
            self.movingDown = not self.movingDown
            if checkHit[2]:
                self.xSpeed *= -1
                self.movingRight = not self.movingRight
            self.ySpeed *= -1
            self.blocks.numBlocks -= 1
            self.points -= 10
        if self.yCoordBall >= self.height or self.yCoordBall <= 0:
            self.hitSound.play()
            self.movingDown = not self.movingDown
            if self.yCoordBall >= self.height:
                self.gameOver()
        self.numBlocks = self.blocks.isEmpty()
        if self.yCoordBall <= 0:
            self.LevelUp()
        if self.xCoordBall >= self.width or self.xCoordBall <= 0:
            self.hitSound.play()
            #WALL
            self.xSpeed *= -1
            self.movingRight = not self.movingRight
        if self.yCoordBall >= self.height or self.yCoordBall <= 0:
            #CEILING
            self.ySpeed *= -1
            self.movingDown = not self.movingDown

    def drawBricks(self):
        for i in range(len(self.blocks.getBlocks())):
                for j in range(len(self.blocks.getBlocks()[i])):
                    if self.blocks.getBlocks()[i][j].checkVisible():
                        if self.blocks.getBlocks()[i][j].getSpecial() == "bomb":
                            tup = self.blocks.getBlocks()[i][j].getColor()
                            pygame.draw.rect(self.screen, self.blocks.getBlocks()[i][j].getColor(), (self.blocks.getBlocks()[i][j].getXCoord(), self.blocks.getBlocks()[i][j].getYCoord(), self.blocks.getBlocks()[i][j].getWidth(), self.blocks.getBlocks()[i][j].getHeight()),0)
                            pygame.draw.circle(self.screen, (255 - tup[0], 255 - tup[1], 255 - tup[2]), (self.blocks.getBlocks()[i][j].getXCoord()+(12),self.blocks.getBlocks()[i][j].getYCoord()+(5)), 3, 0)
                        elif self.blocks.getBlocks()[i][j].getSpecial() == "life":
                            img = pygame.transform.scale(heartImage, (self.blocks.getBlocks()[i][j].getWidth(), self.blocks.getBlocks()[i][j].getHeight()))
                            rect = pygame.draw.rect(self.screen, self.white, (self.blocks.getBlocks()[i][j].getXCoord(), self.blocks.getBlocks()[i][j].getYCoord(), self.blocks.getBlocks()[i][j].getWidth(), self.blocks.getBlocks()[i][j].getHeight()),0)
                            self.screen.blit(img, rect)
                        else:
                            pygame.draw.rect(self.screen, self.blocks.getBlocks()[i][j].getColor(), (self.blocks.getBlocks()[i][j].getXCoord(), self.blocks.getBlocks()[i][j].getYCoord(), self.blocks.getBlocks()[i][j].getWidth(), self.blocks.getBlocks()[i][j].getHeight()),0)

    def playGame(self):
        startTick = pygame.time.get_ticks()
        while True:
            self.timeGone = (pygame.time.get_ticks() - startTick)/1000
            if 3 - self.timeGone <= 0:
                break
            timeLeft = self.font.render("Time Until Start " + str(round(3 - self.timeGone, 1)), True, (255, 255, 0))
            self.screen.blit(timeLeft, [(self.width / 2) - 50, self.height - (self.height / 5)])
            self.draw()
            self.drawBricks()
            pygame.time.delay(20)
            pygame.display.flip()
            self.screen.fill(self.black)

        while self.stillPlaying:
            self.pointtime += 0.5
            if self.pointtime == 20:
                self.pointtime = 0
                self.points -= 1
            
            
            self.draw()
            self.drawBricks()
            #print("Rect ("+str(self.xCoordPaddle)+", "+str(self.yCoordPaddle)+")")
            #print("Ball ("+str(self.xCoordBall)+", "+str(self.yCoordBall)+")")
            pygame.time.delay(20)

            pygame.key.set_repeat(1, 100)
        
            pygame.display.flip()
                
            self.checkInputs()
            self.checkCollisions()
            
            #print((self.yCoordBall >= self.yCoordPaddle and self.yCoordBall <= self.yCoordPaddle + self.paddleHeight))
            #print((self.xCoordBall >= self.xCoordPaddle and self.xCoordBall <= self.xCoordPaddle + self.paddleWidth))
            
            self.yCoordBall += self.ySpeed
            self.xCoordBall += self.xSpeed
            #self.draw()

            self.screen.fill(self.black)

        return self.levelUp, self.restartLevel, self.restartGame

game = Breakout()
game.mainMenu()
while 1:
    levelUp, restartLevel, restartGame = game.playGame()
    if game.playAgain:
        game.restart(levelUp, restartLevel, restartGame)
    else:
        break
