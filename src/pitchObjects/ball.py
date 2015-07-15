import pygame
import math
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GAME_FPS, GRAPH_BALL_SIZE, MECH_BALL_SPEED, MECH_BALL_SIZE, MECH_TURNS_RECOVERING
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
        self.isOutOfPlay = True

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

        self.velX = (goalX - self.posX)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED
        self.velY = (goalY - self.posY)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED

    def passTo(self, player):
        print "Passed"
        self.kicked()
        self.target = player

        self.velX = (player.posX - self.posX)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED
        self.velY = (player.posY - self.posY)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED

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
        self.isOutOfPlay = False

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
                if player.team.isDefendingLeft:
                    controlVal += 1
                else:
                    controlVal -= 1

            for player in players:
                if not player.recovering:
                    if self.possessor:
                        if controlVal == 0:
                            winningPlayer = player
                            break
                        elif controlVal > 0 and self.possessor.team.isDefendingLeft:
                            winningPlayer = self.possessor
                            break
                        elif controlVal > 0:
                            if player.team.isDefendingLeft:
                                winningPlayer = player
                                break
                        elif controlVal < 0 and not self.possessor.team.isDefendingLeft:
                            winningPlayer = self.possessor
                            break
                        else:
                            if not player.team.isDefendingLeft:
                                winningPlayer = player
                                break
                    else:
                        if controlVal == 0:
                            winningPlayer = player
                        elif controlVal > 0:
                            if player.team.isDefendingLeft:
                                winningPlayer = player
                                break
                        else:
                            if not player.team.isDefendingLeft:
                                winningPlayer = player
                                break

        if winningPlayer:
            if self.possessor != winningPlayer:
                if self.possessor:
                    self.possessor.recovering = MECH_TURNS_RECOVERING
                    self.possessor.hasBall = False
                self.possessor = winningPlayer

            self.target = None
            self.isLoose = False
            self.possessor.hasBall = True
            self.possessionController.setPossession(self.possessor.team)


    def checkOutOfBounds(self):
        """keep players from running out of bounds"""
        if self.posX > FIELD_LENGTH + MECH_BALL_SIZE:
            self.posX = FIELD_LENGTH + MECH_BALL_SIZE
            self.outOfBounds()
        if self.posX < 0 - MECH_BALL_SIZE:
            self.posX = 0 - MECH_BALL_SIZE
            self.outOfBounds()
        if self.posY > FIELD_WIDTH + MECH_BALL_SIZE:
            self.posY = FIELD_WIDTH + MECH_BALL_SIZE
            self.outOfBounds()
        if self.posY < 0 - MECH_BALL_SIZE:
            self.posY = 0 - MECH_BALL_SIZE
            self.outOfBounds()

    def outOfBounds(self):
        self.velX = 0
        self.velY = 0
        self.isOutOfPlay = True
        self.possessionController.switchPossession(self)
