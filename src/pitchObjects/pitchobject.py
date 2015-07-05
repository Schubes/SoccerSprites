import pygame
from display.displaymapper import convertFieldPosition

__author__ = 'Thomas'

class PitchObject(pygame.sprite.DirtySprite):
    """Super class for fieldPlayers and ball"""
    def __init__(self, pitchSurface, color):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface([10, 10])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.posX = self.getStartingPosX()
        self.posY = self.getStartingPosY()
        self.pitchSurface = pitchSurface
        self.color = color
        self.dirty = 2

    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY