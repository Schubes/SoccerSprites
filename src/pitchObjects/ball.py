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
        self.turnsUntouchable = 0

        self.velX = 0
        self.velY = 0

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self):
        print "Shot Fired!"


        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True

        #TODO: make the players kick a bit harder
        self.posX = self.posX
        self.posY = self.posY

    def passTo(self, player):
        assert self.possessor is not None
        assert self.possessor.hasBall
        assert self.possessor.team.hasPossession

        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True

        distanceToPlayer = math.sqrt((player.posX - self.posX)**2 + (player.posY - self.posY)**2)
        #the idea is that you kick the ball faster if it is going further, but it's not linear
        self.velX = (player.posX - self.posX)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED
        self.velY = (player.posY - self.posY)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED

    def update(self,players):
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
                #remove possesion from previous team
                if self.attackingTeam:
                    self.attackingTeam.hasPossession = False
                    if self.possessor:
                        self.possessor.hasBall = False

                #select the first player who touched the ball
                if len(players) > 1:
                    if players[0] == self.possessor:
                        self.possessor = players[1]
                    else:
                        self.possessor = players[0]
                else:
                    self.possessor = players[0]
                #set new possesion
                self.isLoose = False
                self.attackingTeam = players[0].team
                self.possessor.hasBall = True
                self.possessor.team.hasPossession = True
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