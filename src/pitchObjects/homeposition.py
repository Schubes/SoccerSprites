import pygame
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import STRAT_HOME_POS_SIZE, COLOR_ORANGE
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class HomePosition(PitchObject):
    """
    This class defines the area of the field that a particular player is responsible for at any given moment.
    """
    def __init__(self, playerRole, team, ball):
        self.team = team
        self.ball = ball

        self.perX = playerRole[0]
        self.perY = playerRole[1]

        self.defaultPosX = self.perX * FIELD_LENGTH/2
        self.defaultPosY = self.perY * FIELD_WIDTH

        PitchObject.__init__(self, COLOR_ORANGE, self.defaultPosX, self.defaultPosY, STRAT_HOME_POS_SIZE)

    def update(self):
        self.move()
        PitchObject.update(self)

    def move(self):
        self.posX = self.relX(self.defaultPosX + self.attackingModifierX() + self.ballModifierX() + self.setPiecesModifierX(), self.team.isDefendingLeft)
        self.posY = self.defaultPosY + self.ballModifierY() + self.defendingModifierY()

    def ballModifierX(self):
        if self.ball.getDistanceToGoalline(True, self.team.isDefendingLeft):
            return (float(self.ball.getDistanceToGoalline(False, self.team.isDefendingLeft)) - FIELD_LENGTH/4)/2
        return 0

    def ballModifierY(self):
        overloadingBox = 0
        if self.posX < 30 or self.posX > 90:
            overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY) * ((abs(60 - self.posX))-30)/50
        return overloadingBox

    def defendingModifierY(self):
        if not self.team.hasPossession:
            return (self.ball.posY - self.defaultPosY)/FIELD_WIDTH
        else:
            return 0

    def attackingModifierX(self):
        if self.team.hasPossession:
            push = self.ball.possessionController.getRecentPossessionTime()/250
            return 20
        else:
            return 0


    def setPiecesModifierX(self):
        if (self.ball.outOfPlay is "CornerKick"):
            if self.team.hasPossession:
                return 20
            else:
                return -20
        return 0