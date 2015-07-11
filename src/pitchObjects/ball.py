import pygame
import math
from gamevariables import FIELD_LENGTH, FIELD_WIDTH, COLOR_BALL, GAME_FPS, COLOR_PAINT
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self):
        PitchObject.__init__(self, COLOR_BALL, self.getStartingPosX(), self.getStartingPosY())
        self.image = pygame.Surface([20, 20])
        self.image.fill(COLOR_BALL)
        self.rect = self.image.get_rect()

        self.closetDefender = self.getClosetDefender()
        self.possessor = None
        self.velX = 0
        self.velY = 0

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self):
        self.possessor = None
        #TODO: make the players kick a bit harder
        self.posX = self.posX
        self.posY = self.posY

    def passTo(self, player):
        assert self.possessor is not None
        assert self.possessor.hasBall
        self.possessor.hasBall = False
        self.possessor.team.hasPossession = False
        self.possessor = None
        #for better visualization of who has the ball
        distanceToPlayer = math.sqrt((player.posX - self.posX)**2 + (player.posY - self.posY)**2)
        #the idea is that you kick the ball faster if it is going further, but it's not linear
        self.velX = math.sqrt(distanceToPlayer) * (player.posX - self.posX)/20
        self.velY = math.sqrt(distanceToPlayer) * (player.posY - self.posY)/20

    def update(self,players):
        self.turnResult(players)
        PitchObject.update(self)

    def turnResult(self, players):
        #if there is a player controlling the ball, the ball should move with that player
        if self.possessor is not None:
            self.posX = self.possessor.posX
            self.posY = self.possessor.posY
            self.velX = 0
            self.velY = 0
        else:
            self.posX += self.velX / GAME_FPS
            self.posY += self.velY / GAME_FPS
        if self.possessor:
            self.possessor.hasBall = False
            self.possessor.team.hasPossession = False

        players = pygame.sprite.spritecollide(self, players, False)
        if players:
            self.possessor = players[0]
            players[0].hasBall = True
            players[0].team.hasPossession = True



    def getClosetDefender(self):
        pass

    def getPossesor(self):
        pass