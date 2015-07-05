import pygame
from display.displaymapper import convertFieldPosition

__author__ = 'Thomas'

class PitchObject(pygame.sprite.DirtySprite):
    """Super class for fieldPlayers and ball"""
    def __init__(self, pitchSurface, color, posX, posY):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface([10, 10])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.startingPosX = posX
        self.startingPosY = posY

        self.posX = posX
        self.posY = posY
        self.pitchSurface = pitchSurface
        self.color = color
        self.dirty = 2

    def update(self):
        self.rect.topleft = convertFieldPosition(self.posX, self.posY)