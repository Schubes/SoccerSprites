import math
from gamevariables import FIELD_LENGTH, FIELD_WIDTH, GAME_FPS, STRAT_NEARBALL, STRAT_SHOOTINGRANGE, ATTR_PLAYERSPEED
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class FieldPlayer(PitchObject):
    """Class for players currently on the pitch"""
    def __init__(self, playerRole, team, ball, posX, posY):
        """
        playerRole is a string ("gk", "lb", "cb", etc...)
        """
        PitchObject.__init__(self, team.color, posX, posY)
        self.playerRole = playerRole
        self.team = team
        self.shootingRange = STRAT_SHOOTINGRANGE
        self.hasBall = False
        self.ball = ball
        self.isOffsides = False
        self.covering = []
        self.blocking = []
        self.isBlockedBy = []
        self.isCoveredBy = []
        self.speed = float(ATTR_PLAYERSPEED)

    def isInShootingRange(self):
        if self.getWeightedDistanceToGoal(True) < self.shootingRange:
            return True
        else:
            return False

    def update(self, grandObserver):
        self.makeAction(grandObserver)
        self.confirmInBounds()
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
        #TODO: Clean this up
        if self.isOffsides:
            self.posX -= self.dirX(self.speed)
        else:
            if self.ball.isLoose:
                if self.nearBall():
                    self.chase(self.ball)
                else:
                    self.posX += self.dirX(self.speed)
            else:
                self.posX += self.dirX(self.speed)

    def defend(self):
        if self.nearBall():
            self.chase(self.ball)
        elif self.covering:
            self.chase(self.covering[0])
        else:
            self.reposition()

    def nearBall(self):
        if self.squaredDistanceTo(self.ball) < STRAT_NEARBALL:
            return True
        else:
            return False

    def chase(self, pitchObject):
        #TODO: eventually want to factor in dervatives of position
        difX = pitchObject.posX - self.posX
        difY = pitchObject.posY - self.posY
        dif = abs(difX) + abs(difY)
        if not dif == 0:
            self.posX += self.dirX(float(difX)/dif * self.speed)
            self.posY += float(difY)/dif * self.speed

    def reposition(self):
        if self.playerRole < 3 and self.ball.getDistanceToGoalline(False, self.team.isDefendingLeft) < \
                        self.getDistanceToGoalline(False) + 10:
            self.posX -= self.dirX(self.speed)
        elif self.isOffsides:
            self.posX -= self.dirX(self.speed)

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
        return self.getDistanceToGoalline(attacking)*10 + (self.posY-FIELD_WIDTH/2)**2

    def getDistanceToGoalline(self, attacking):
        return PitchObject.getDistanceToGoalline(self, attacking, self.team.isDefendingLeft)

    def dirX(self, horizontalValue):
        if self.team.isDefendingLeft:
            return horizontalValue
        else:
            return - horizontalValue