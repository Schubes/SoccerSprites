from gamevariables import FIELD_LENGTH, FIELD_WIDTH, GAME_FPS
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

needsToBeImplemented = 5

class FieldPlayer(PitchObject):
    """Class for players currently on the pitch"""
    def __init__(self, playerRole, team, ball, posX, posY):
        """
        playerRole is a string ("gk", "lb", "cb", etc...)
        """
        PitchObject.__init__(self, team.color, posX, posY)
        self.playerRole = playerRole
        self.team = team
        self.shootingRange = needsToBeImplemented
        self.hasBall = False
        self.ball = ball
        self.isOffsides = False
        self.covering = []
        self.blocking = []
        self.isBlockedBy = []
        self.isCoveredBy = []

    def isInShootingRange(self):
        if self.getWeightedDistanceToGoal(True) < self.shootingRange:
            return True
        else:
            return False

    def update(self, grandObserver):
        self.makeAction(grandObserver)
        PitchObject.update(self)

    def makeAction(self, grandObserver):
        if self.team.hasPossession:
            if self.hasBall:
                self.makePlay(grandObserver)
            else:
                self.makeRun()
        else:
            self.defend()

    def makePlay(self, grandObserver):
        if self.isInShootingRange():
            self.ball.simShot()
        else:
            bestPassOption = self
            for openPlayer in grandObserver.openPlayers:
                if openPlayer.getDistanceToGoalline(True) < bestPassOption.getDistanceToGoalline(True):
                    bestPassOption = openPlayer
            if bestPassOption is not self:
                self.ball.passTo(bestPassOption)
            else:
                self.makeRun()

    def makeRun(self):
        #TODO: Make players less stupid
        self.posX += float(needsToBeImplemented)/GAME_FPS
        self.confirmInBounds()

    def defend(self):
        pass

    def confirmInBounds(self):
        """keep players from running out of bounds"""
        if self.posX > FIELD_LENGTH:
            self.posX = FIELD_LENGTH
        if self.posX < 0:
            self.posX = 0
        if self.posY > FIELD_WIDTH:
            self.posY = FIELD_WIDTH
        if self.posY < 0:
            self.posY = 0

    def getWeightedDistanceToGoal(self, attacking):
        return self.getDistanceToGoalline(attacking) + (self.posY-FIELD_WIDTH/2)**2

    def getDistanceToGoalline(self, attacking):
        if self.team.isDefendingLeft and not attacking:
            return self.posX
        elif not self.team.isDefendingLeft and attacking:
            return self.posX
        else:
            return abs(self.posX-FIELD_LENGTH)