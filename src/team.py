from gamevariables import FIELD_LENGTH, FIELD_WIDTH
from pitchObjects.fieldplayer import FieldPlayer

__author__ = 'Thomas'

class Team:
    def __init__(self,isDefendingLeft, color):
        self.isDefendingLeft = isDefendingLeft
        self.hasPossession = isDefendingLeft
        self.color = color
        self.players = []

    def setStartingLineUp(self, formation, ball, window):
        players = []
        if self.isDefendingLeft:
            players.append(FieldPlayer("GK", self, ball, 5, FIELD_WIDTH/2))
        else:
            players.append(FieldPlayer("GK", self, ball, (FIELD_LENGTH - 5), FIELD_WIDTH/2))
        for lineNum, line in enumerate(formation):
            for posNum, position in enumerate(range(line)):
                if self.isDefendingLeft:
                    posX = float(lineNum + 1)/len(formation) * FIELD_LENGTH/2
                else:
                    posX = FIELD_LENGTH - (float(lineNum + 1)/len(formation) * FIELD_LENGTH/2)
                posY = float(posNum+.5)/line * FIELD_WIDTH
                players.append(FieldPlayer(lineNum, self, ball, posX, posY))
        self.players = players
        return players
