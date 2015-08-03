import pygame
import math
from abc import ABCMeta, abstractmethod
from display.displaymapper import convertFieldPosition, FIELD_LENGTH
from gamevariables import GAME_FPS

__author__ = 'Thomas'

class PitchObject(pygame.sprite.DirtySprite):
    """Super class for fieldPlayers and ball"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, color, posX, posY, size):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.image.set_alpha(180)

        self.rect = self.image.get_rect()

        self.startingPosX = posX
        self.startingPosY = posY

        self.posX = posX
        self.posY = posY
        self.velX = 0
        self.velY = 0

        self.color = color
        self.dirty = 2

    @abstractmethod
    def update(self):
        """
        Updates the location on the screen. Any child objects should call this method if they are being displayed.

        :return:
        """
        self.rect.center = convertFieldPosition(self.posX, self.posY)

    @abstractmethod
    def move(self):
        self.posX += self.velX / GAME_FPS
        self.posY += self.velY / GAME_FPS

    def getDistanceToGoalline(self, attacking, isDefendingLeft):
        if isDefendingLeft and not attacking:
            return self.posX
        elif not isDefendingLeft and attacking:
            return self.posX
        else:
            return abs(self.posX-FIELD_LENGTH)

    def getDistanceTo(self, pitchObject):
        return math.sqrt(((self.posX - pitchObject.posX)**2) + ((self.posY - pitchObject.posY)**2))

    def relX(self, posX, defendingLeft):
        if defendingLeft:
            return posX
        else:
            return FIELD_LENGTH - posX