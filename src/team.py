from gamevariables import FIELD_LENGTH, FIELD_WIDTH
from pitchObjects.fieldPlayer import FieldPlayer

__author__ = 'Thomas'

class Team:
    def __init__(self,isDefendingLeft, color):
        self.isDefendingLeft = isDefendingLeft
        self.hasPossession = isDefendingLeft
        self.color = color

    def setStartingLineUp(self, formation, ball, window):
        teamPlayers = []
        teamPlayers.append(FieldPlayer("GK", self, ball, window, 5, FIELD_WIDTH/2))
        if self.isDefendingLeft:
            formationIter = iter(formation)
        else:
            formationIter = reversed(formation)
        for lineNum, line in enumerate(formationIter):
            for posNum, position in enumerate(range(line)):
                if self.isDefendingLeft:
                    posX = float(lineNum + 1)/len(formation) * FIELD_LENGTH/2
                else:
                    posX = FIELD_LENGTH - (float(lineNum + 1)/len(formation) * FIELD_LENGTH/2)
                posY = float(posNum+.5)/line * FIELD_WIDTH
                teamPlayers.append(FieldPlayer("", self, ball, window, posX, posY))
        return teamPlayers
