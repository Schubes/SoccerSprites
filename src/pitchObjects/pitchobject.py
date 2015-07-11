import pygame
from display.displaymapper import convertFieldPosition
from gamevariables import FIELD_LENGTH

__author__ = 'Thomas'

class PitchObject(pygame.sprite.DirtySprite):
    """Super class for fieldPlayers and ball"""
    def __init__(self, color, posX, posY):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface([10, 10])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.startingPosX = posX
        self.startingPosY = posY

        self.posX = posX
        self.posY = posY
        self.color = color
        self.dirty = 2

    def update(self):
        self.rect.center = convertFieldPosition(self.posX, self.posY)

    def getDistanceToGoalline(self, attacking, isDefendingLeft):
        if isDefendingLeft and not attacking:
            return self.posX
        elif not isDefendingLeft and attacking:
            return self.posX
        else:
            return abs(self.posX-FIELD_LENGTH)

    def squaredDistanceTo(self, pitchObject):
        return ((self.posX - pitchObject.posX)**2) + ((self.posY - pitchObject.posY)**2)