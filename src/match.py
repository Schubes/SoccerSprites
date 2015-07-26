import pygame
from controllers.possessioncontroller import PossessionController
from display.displaymapper import convertFieldPosition, convertYards2Pixels, FIELD_LENGTH, FIELD_WIDTH, WINDOW_HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from gamevariables import COLOR_TEAM_BLUE, COLOR_TEAM_RED, COLOR_GRASS, COLOR_PAINT, PAINT_WIDTH, COLOR_HEADER
from grandobserver import GrandObserver
from pitchObjects.ball import Ball
from team import Team

__author__ = 'Thomas'

class Match:
    """Handles match gameplay"""
    def __init__(self, window):
        self.window = window

        self.header = self.createHeader()
        self.headerBG = self.createHeader()

        self.pitchSurface = self.createPitchSurface()
        self.fieldBackground = self.createPitchSurface()

        self.team1 = Team(True, COLOR_TEAM_BLUE, "Blue Team")
        self.team2 = Team(False, COLOR_TEAM_RED, "Red Team")

        self.possessionController = PossessionController(self.team1, self.team2)

        self.ball = Ball(self.possessionController)
        self.ballGroup = pygame.sprite.LayeredDirty(self.ball)

        #PLAYERS
        self.allPlayers = pygame.sprite.LayeredDirty()
        self.team1.setStartingLineUp((4, 3, 3), self.ball, window)
        self.allPlayers.add(self.team1.players)
        self.team2.setStartingLineUp((4, 3,3), self.ball, window)
        self.allPlayers.add(self.team2.players)

        #OBJECTS TO BE DRAWN
        self.allPitchObjects = pygame.sprite.LayeredDirty(self.allPlayers, self.ballGroup, self.team1.goal, self.team2.goal)
        self.allPitchObjects.move_to_back(self.ball)

        self.ball.posX = FIELD_LENGTH/2
        self.ball.posY = FIELD_WIDTH/2

        self.grandObserver = GrandObserver(self.team1, self.team2, self.ball)

        self.startTime = pygame.time.get_ticks()


    def playMatchTurn(self):
        self.grandObserver.analyze()
        self.allPlayers.update(self.grandObserver)
        self.ballGroup.update(self.allPlayers)
        self.allPitchObjects.draw(self.pitchSurface)
        self.allPitchObjects.clear(self.pitchSurface, self.fieldBackground)
        self.window.blit(self.pitchSurface, (0, WINDOW_HEADER_HEIGHT))
        self.window.blit(self.header, (0, 0))


    def createPitchSurface(self):
        pitchSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - WINDOW_HEADER_HEIGHT))
        pitchSurface.fill(COLOR_GRASS)

        #Top Line
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(0, 0), convertFieldPosition(FIELD_LENGTH, 0), PAINT_WIDTH)

        #Bottom Line
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(0, FIELD_WIDTH), convertFieldPosition(FIELD_LENGTH, FIELD_WIDTH), PAINT_WIDTH)

        #Middle Line
        pygame.draw.circle(pitchSurface, COLOR_PAINT, convertFieldPosition(FIELD_LENGTH/2, FIELD_WIDTH/2), convertYards2Pixels(10), PAINT_WIDTH)
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(FIELD_LENGTH/2, 0), convertFieldPosition(FIELD_LENGTH/2, FIELD_WIDTH), PAINT_WIDTH)

        #LEFT SIDE
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(0, 0), convertFieldPosition(0, FIELD_WIDTH), PAINT_WIDTH)

        centerOfGoalLine = convertFieldPosition(0, FIELD_WIDTH/2)

        sixYardBox = pygame.Rect(centerOfGoalLine[0], (centerOfGoalLine[1] - convertYards2Pixels(10)), convertYards2Pixels(6), convertYards2Pixels(20))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, sixYardBox, PAINT_WIDTH)

        plenaltyBox = pygame.Rect(centerOfGoalLine[0], (centerOfGoalLine[1] - convertYards2Pixels(22)), convertYards2Pixels(18), convertYards2Pixels(44))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, plenaltyBox, PAINT_WIDTH)

        #RIGHT SIDE
        pygame.draw.line(pitchSurface, COLOR_PAINT, convertFieldPosition(FIELD_LENGTH, 0), convertFieldPosition(FIELD_LENGTH, FIELD_WIDTH), PAINT_WIDTH)

        centerOfGoalLine = convertFieldPosition(FIELD_LENGTH, FIELD_WIDTH/2)

        sixYardBox = pygame.Rect((centerOfGoalLine[0] - convertYards2Pixels(6)) , (centerOfGoalLine[1] - convertYards2Pixels(10)), convertYards2Pixels(6), convertYards2Pixels(20))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, sixYardBox, PAINT_WIDTH)

        plenaltyBox = pygame.Rect((centerOfGoalLine[0] - convertYards2Pixels(18)), (centerOfGoalLine[1] - convertYards2Pixels(22)), convertYards2Pixels(18), convertYards2Pixels(44))
        pygame.draw.rect(pitchSurface, COLOR_PAINT, plenaltyBox, PAINT_WIDTH)


        return pitchSurface

    def createHeader(self):
        header = pygame.Surface((WINDOW_WIDTH, WINDOW_HEADER_HEIGHT))
        header.fill(COLOR_HEADER)

        return header
