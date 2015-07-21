import random
import pygame
import math
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GRAPH_BALL_SIZE, MECH_BALL_SPEED, MECH_BALL_SIZE, MECH_TURNS_RECOVERING, \
    MECH_PASS_VEL_MODIFIER
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self, possessionController):
        PitchObject.__init__(self, COLOR_BALL, self.getStartingPosX(), self.getStartingPosY(), GRAPH_BALL_SIZE)
        self.image.set_alpha(255)

        self.possessionController = possessionController
        self.possessor = None
        self.prevPossessor = None
        self.isLoose = True
        self.target = True
        self.outOfPlay = "Kickoff"

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self, rightGoal):
        print "Shot Fired!"
        self.kicked()
        self.possessionController.noPossession()

        goalY = FIELD_WIDTH/2
        if rightGoal:
            goalX = FIELD_LENGTH
        else:
            goalX = 0

        self.velX = (goalX - self.posX)/(math.sqrt((goalY - self.posY)**2 + (goalX - self.posX)**2)) * MECH_BALL_SPEED
        self.velY = (goalY - self.posY)/(math.sqrt((goalY - self.posY)**2 + (goalX - self.posX)**2)) * MECH_BALL_SPEED

    def passTo(self, player):
        print "Passed"
        self.kicked()
        self.target = player

        difX = player.posX - self.posX + player.velX / MECH_PASS_VEL_MODIFIER #Just a magic number that works well
        difY = player.posY - self.posY + player.velY / MECH_PASS_VEL_MODIFIER
        difMag = math.sqrt(difX**2 + difY**2)

        self.velX = difX/difMag * MECH_BALL_SPEED
        self.velY = difY/difMag * MECH_BALL_SPEED

    def kicked(self):
        """sets properties when ball is willingly given up"""
        assert self.possessor is not None
        assert self.possessor.hasBall
        assert self.possessor.team.hasPossession

        self.possessor.hasBall = False
        self.possessor.recovering = MECH_TURNS_RECOVERING
        self.prevPossessor = self.possessor
        self.possessor = None
        self.isLoose = True
        self.outOfPlay = None

    def update(self, players):
        self.moveBall()
        self.checkOutOfBounds()
        self.evaluateControl(players)
        PitchObject.update(self)

    def moveBall(self):
        #if there is a player controlling the ball, the ball should move with that player
        if self.possessor is not None:
            self.posX = self.possessor.posX
            self.posY = self.possessor.posY
            self.velX = 0
            self.velY = 0
        else:
            PitchObject.move(self)

    def evaluateControl(self, players):
        players = pygame.sprite.spritecollide(self, players, False)
        winningPlayer = None
        if players:
            controlVal = 0

            for player in players:
                if self.possessor:
                    if player.team is self.possessor.team:
                        controlVal += 1
                    else:
                        controlVal -= 1

                    for player in players:
                        if not player.recovering:
                            if controlVal > 0:
                                winningPlayer = self.possessor
                                break
                            elif controlVal <= 0:
                                if player.team.isDefendingLeft:
                                    winningPlayer = player
                                    break
                else:
                    if not player.recovering:
                        winningPlayer = random.choice(players)

        if winningPlayer:
            if self.possessor != winningPlayer:
                if self.possessor:
                    self.possessor.recovering = MECH_TURNS_RECOVERING
                    self.possessor.hasBall = False
                    self.prevPossessor = self.possessor
                self.possessor = winningPlayer

            self.target = None
            self.isLoose = False
            self.possessor.hasBall = True
            self.possessionController.setPossession(self.possessor.team)

            if winningPlayer.isOffsides and self.isLoose and not self.outOfPlay:
                print "OFFSIDES!!!!"
                self.linesPersonRuling("SetPiece")


    def checkOutOfBounds(self):
        """keep players from running out of bounds"""
        if self.posX > FIELD_LENGTH + MECH_BALL_SIZE:
            self.posX = FIELD_LENGTH + MECH_BALL_SIZE
            if self.blameTeam():
                self.posX = FIELD_LENGTH - 6
                self.linesPersonRuling("GoalKick")
            else:
                self.posX = FIELD_LENGTH
                self.linesPersonRuling("CornerKick")

        if self.posX < 0 - MECH_BALL_SIZE:
            if self.blameTeam():
                self.posX = 0
                self.linesPersonRuling("CornerKick")
            else:
                self.posX = 6
                self.linesPersonRuling("GoalKick")

        if self.posY > FIELD_WIDTH + MECH_BALL_SIZE:
            self.posY = FIELD_WIDTH + MECH_BALL_SIZE
            self.linesPersonRuling("ThrowIn")

        if self.posY < 0 - MECH_BALL_SIZE:
            self.posY = 0 - MECH_BALL_SIZE
            self.linesPersonRuling("ThrowIn")

    def blameTeam(self):
        assert self.possessor or self.prevPossessor
        if self.possessor:
            return self.possessor.team.isDefendingLeft
        if self.prevPossessor:
            return self.prevPossessor.team.isDefendingLeft

    def linesPersonRuling(self, typeOfPlay):
        if typeOfPlay is "CornerKick":
            if self.posY > FIELD_WIDTH/2:
                self.posY = FIELD_WIDTH
            else:
                self.posY = 0
        elif typeOfPlay is "GoalKick":
            if self.posY > FIELD_WIDTH/2:
                self.posY = FIELD_WIDTH/2 + 10
            else:
                self.posY = FIELD_WIDTH/2 - 10

        self.velX = 0
        self.velY = 0

        self.outOfPlay = typeOfPlay
        if self.possessor:
            self.possessor.hasBall = False
        self.possessionController.switchPossession(self)
        self.prevPossessor = self.possessor
        self.possessor = None
