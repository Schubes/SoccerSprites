import pygame
import math
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GAME_FPS, MECH_TURNS_UNTOUCHABLE, GRAPH_BALL_SIZE, MECH_BALL_SPEED
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self):
        PitchObject.__init__(self, COLOR_BALL, self.getStartingPosX(), self.getStartingPosY(), GRAPH_BALL_SIZE)

        self.closetDefender = self.getClosetDefender()
        self.possessor = None
        self.attackingTeam = None
        self.isLoose = True
        self.target = True
        self.turnsUntouchable = 0

        self.velX = 0
        self.velY = 0

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self, rightGoal):
        print "Shot Fired!"

        self.possessor.team.hasPossession = False
        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True

        goalY = FIELD_WIDTH/2
        if rightGoal:
            goalX = FIELD_LENGTH
        else:
            goalX = 0

        self.velX = (goalX - self.posX)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED
        self.velY = (goalY - self.posY)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED

    def passTo(self, player):
        assert self.possessor is not None
        assert self.possessor.hasBall
        assert self.possessor.team.hasPossession

        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True
        self.target = player

        distanceToPlayer = math.sqrt((player.posX - self.posX)**2 + (player.posY - self.posY)**2)
        #the idea is that you kick the ball faster if it is going further, but it's not linear
        self.velX = (player.posX - self.posX)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED
        self.velY = (player.posY - self.posY)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED

    def update(self, players):
        self.moveBall()
        self.confirmInBounds()
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
            self.posX += self.velX / GAME_FPS
            self.posY += self.velY / GAME_FPS

    def evaluateControl(self, players):
        if self.turnsUntouchable > 0:
            self.turnsUntouchable -= 1
        else:
            players = pygame.sprite.spritecollide(self, players, False)
            if players:
                controlVal = 0
                for player in players:
                    if player.team.isDefendingLeft:
                        controlVal += 1
                    else:
                        controlVal -= 1
                if len(players) > 1:
                    for player in players:
                        if player != self.possessor:
                            if controlVal == 0:
                                winningPlayer = player
                            elif controlVal > 0:
                                if player.team.isDefendingLeft:
                                    winningPlayer = player
                            else:
                                if not player.team.isDefendingLeft:
                                    winningPlayer = player
                else:
                    winningPlayer = players[0]

                #remove possesion from previous team
                if self.attackingTeam:
                    self.attackingTeam.hasPossession = False
                    if self.possessor:
                        self.possessor.hasBall = False
                self.target = None

                #select the first player who touched the ball
                self.possessor = winningPlayer
                #set new possesion
                self.isLoose = False
                self.attackingTeam = players[0].team
                self.possessor.hasBall = True
                self.attackingTeam.hasPossession = True
                self.turnsUntouchable = MECH_TURNS_UNTOUCHABLE

    def confirmInBounds(self):
        """keep players from running out of bounds"""
        if self.posX > FIELD_LENGTH:
            self.posX = FIELD_LENGTH
        if self.posX < 0:
            self.posX = 0
        if self.posY > FIELD_WIDTH:
            self.posY = FIELD_WIDTH
        if self.posY < 0:
            self.posY = 0


    def getClosetDefender(self):
        pass

    def getPossesor(self):
        pass