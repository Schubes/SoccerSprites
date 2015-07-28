import pygame
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import STRAT_HOME_POS_SIZE, COLOR_ORANGE
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class HomePosition(PitchObject):
    def __init__(self, playerRole, team, ball):
        self.team = team
        self.ball = ball

        self.perX = playerRole[0]
        self.perY = playerRole[1]

        self.defaultPosX = (self.relX(self.perX * FIELD_LENGTH/2, self.team.isDefendingLeft))
        self.defaultPosY = self.perY * FIELD_WIDTH

        PitchObject.__init__(self, COLOR_ORANGE, self.defaultPosX, self.defaultPosY, STRAT_HOME_POS_SIZE)

    def update(self):
        self.posX = self.defaultPosX + self.attackingModifierX() + self.ballModifierX() + self.setPiecesModifierX()
        self.posY = self.defaultPosY + self.ballModifierY() + self.defendingModifierY()

        PitchObject.update(self)

    def ballModifierX(self):
        return 0

    def ballModifierY(self):
        balltracking = (self.ball.posY - FIELD_WIDTH/2) * 2/3 * abs(self.defaultPosY - self.ball.posY)/FIELD_WIDTH
        if self.posX < 30:
            overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(50/(30-self.posX))
        elif self.posX > 90:
            overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(50/(self.posX-90))
        else:
            if self.posX > FIELD_LENGTH/2:
                overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(100/(self.posX + 1 - FIELD_LENGTH))/3
            else:
                overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(100/(self.posX + 1))/3
        return balltracking + overloadingBox

    def defendingModifierY(self):
        if not self.team.hasPossession:
            return (self.ball.posY - self.defaultPosY)/FIELD_WIDTH
        else:
            return 0

    def attackingModifierX(self):
        if self.team.hasPossession:
            push = self.ball.possessionController.getTimeOfPossession()/250
            if self.team.isDefendingLeft:
                return push + 20
            else:
                return push - 20
        else:
            return 0


    def setPiecesModifierX(self):
        if (self.ball.outOfPlay is "GoalKick") or (self.ball.outOfPlay is "CornerKick"):
            if self.team.hasPossession:
                if self.team.isDefendingLeft:
                    return 20
                else:
                    return -20
            else:
                if self.team.isDefendingLeft:
                    return -20
                else:
                    return 20
        return 0