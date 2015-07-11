import pygame
from display.displaymapper import convertFieldPosition, convertYards2Pixels, FIELD_LENGTH, FIELD_WIDTH, WINDOW_HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from gamevariables import COLOR_TEAM_BLUE, COLOR_TEAM_RED, COLOR_GRASS, COLOR_PAINT, PAINT_WIDTH
from grandobserver import GrandObserver
from pitchObjects.ball import Ball
from pitchObjects.fieldplayer import FieldPlayer
from team import Team

__author__ = 'Thomas'

class Match:
    """Handles match gameplay"""
    def __init__(self, window):
        self.window = window

        self.pitchSurface = self.createPitchSurface()
        self.fieldBackground = self.createPitchSurface()

        self.team1 = Team(True, COLOR_TEAM_BLUE, "Blue Team")
        self.team2 = Team(False, COLOR_TEAM_RED, "Red Team")

        self.nonPlayers = pygame.sprite.LayeredDirty()
        self.ball = Ball()
        self.nonPlayers.add(self.ball)

        self.allPlayers = pygame.sprite.LayeredDirty()
        self.team1.setStartingLineUp((4, 4, 2), self.ball, window)
        self.allPlayers.add(self.team1.players)
        self.team2.setStartingLineUp((4, 3, 3), self.ball, window)
        self.allPlayers.add(self.team2.players)

        self.allObjects = pygame.sprite.LayeredDirty(self.allPlayers,self.nonPlayers)
        self.allObjects.move_to_back(self.ball)

        self.ball.posX = 30
        self.ball.posY = 10

        self.grandObserver = GrandObserver(self.team1, self.team2, self.ball)


    def playMatchTurn(self):
        self.grandObserver.analyze()
        self.allPlayers.update(self.grandObserver)
        self.nonPlayers.update(self.allPlayers)
        self.allObjects.draw(self.pitchSurface)
        self.allObjects.clear(self.pitchSurface, self.fieldBackground)
        self.window.blit(self.pitchSurface, (0, WINDOW_HEADER_HEIGHT))


    def createPitchSurface(self):
        pitchSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT-WINDOW_HEADER_HEIGHT))
        pitchSurface.fill(COLOR_GRASS)

        pygame.draw.circle(pitchSurface, COLOR_PAINT, convertFieldPosition(FIELD_LENGTH/2, FIELD_WIDTH/2), convertYards2Pixels(10), PAINT_WIDTH)
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(FIELD_LENGTH/2, 0), convertFieldPosition(FIELD_LENGTH/2, FIELD_WIDTH), PAINT_WIDTH)

        #LEFT SIDE
        centerOfGoalLine = convertFieldPosition(0, FIELD_WIDTH/2)

        sixYardBox = pygame.Rect(centerOfGoalLine[0], (centerOfGoalLine[1] - convertYards2Pixels(14)), convertYards2Pixels(6), convertYards2Pixels(28))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, sixYardBox, PAINT_WIDTH)

        plenaltyBox = pygame.Rect(centerOfGoalLine[0], (centerOfGoalLine[1] - convertYards2Pixels(22)), convertYards2Pixels(18), convertYards2Pixels(44))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, plenaltyBox, PAINT_WIDTH)

        #RIGHT SIDE
        centerOfGoalLine = convertFieldPosition(FIELD_LENGTH, FIELD_WIDTH/2)

        sixYardBox = pygame.Rect((centerOfGoalLine[0] - convertYards2Pixels(6)) , (centerOfGoalLine[1] - convertYards2Pixels(14)), convertYards2Pixels(6), convertYards2Pixels(28))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, sixYardBox, PAINT_WIDTH)

        plenaltyBox = pygame.Rect((centerOfGoalLine[0] - convertYards2Pixels(18)), (centerOfGoalLine[1] - convertYards2Pixels(22)), convertYards2Pixels(18), convertYards2Pixels(44))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, plenaltyBox, PAINT_WIDTH)

        return pitchSurface
