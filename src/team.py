from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from pitchObjects.player.fieldplayer import FieldPlayer
from pitchObjects.goal import Goal
from pitchObjects.player.goalie import Goalie

__author__ = 'Thomas'

class Team:
    def __init__(self, isDefendingLeft, color, name):
        self.isDefendingLeft = isDefendingLeft
        self.goal = Goal(isDefendingLeft)
        self.hasPossession = isDefendingLeft
        self.color = color
        self.players = []
        self.name = name

    def setStartingLineUp(self, formation, ball, window):
        players = []
        #Goalie

        players.append(Goalie(self, ball))

        # FieldPlayers
        for lineNum, line in enumerate(formation):
            for posNum, position in enumerate(range(line)):
                perX = float(lineNum + 1)/len(formation)
                if self.isDefendingLeft:
                    posX = perX * FIELD_LENGTH/2
                else:
                    posX = FIELD_LENGTH - (perX * FIELD_LENGTH/2)
                perY = float(posNum+.5)/line
                posY = perY * FIELD_WIDTH
                players.append(FieldPlayer((perX, perY), self, ball, posX, posY))
        self.players = players
        return players
