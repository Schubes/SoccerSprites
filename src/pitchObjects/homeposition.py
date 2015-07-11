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

        self.defaultPosX = (self.relX(self.perX * FIELD_LENGTH/2, self.team))
        self.defaultPosY = self.perY * FIELD_WIDTH

        PitchObject.__init__(self, COLOR_ORANGE, self.defaultPosX, self.defaultPosY, STRAT_HOME_POS_SIZE)

    def update(self):
        self.posX = self.defaultPosX + self.attackingModifierX() + self.ballModifierX() #+ self.attackingModifierX()
        self.posY = self.defaultPosY + self.ballModifierY()
        PitchObject.update(self)

    def ballModifierX(self):
        return (self.ball.posX - FIELD_LENGTH/2)/4
        # relX = self.relX(self.defaultPosX, self.team)
        # assert self.relX(relX, self.team) == self.defaultPosX
        # return -self.relX(relX/2, self.team)
        #return self.relX()
        #return -self.relX(self.relX(self.defaultPosX, self.team) * (((FIELD_LENGTH/2) - self.ball.posX) / FIELD_LENGTH), self.team)

    def ballModifierY(self):
        balltracking = (self.ball.posY - FIELD_WIDTH/2) * 2/3 * abs(self.defaultPosY - self.ball.posY)/FIELD_WIDTH
        if self.posX < 30:
            overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(60/(30-self.posX))
        elif self.posX > 90:
            overloadingBox = (FIELD_WIDTH/2 - self.defaultPosY)/(60/(self.posX-90))
        else:
            overloadingBox = 0
        return balltracking + overloadingBox


    def attackingModifierX(self):
        if self.team.hasPossession:
            if self.team.isDefendingLeft:
                return self.defaultPosX
            else:
                return self.defaultPosX - FIELD_LENGTH
        else:
            return 0