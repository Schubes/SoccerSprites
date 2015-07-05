__author__ = 'Thomas'

class Team:
    def __init__(self,isDefendingLeft, color):
        self.isDefendingLeft = isDefendingLeft
        self.hasPossession = isDefendingLeft
        self.color = color

    def isDefendingLeft(self):
        return self.isDefendingLeft

    def getHasPossession(self):
        return self.hasPossession
