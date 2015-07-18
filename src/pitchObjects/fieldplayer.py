import pygame
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import STRAT_NEAR_BALL, ATTR_PLAYER_SPEED, ATTR_SHOOTING_RANGE, GRAPH_PLAYER_SIZE, ATTR_PLAYER_ACCEL, \
    STRAT_MIN_PASS, STRAT_TRY_CROSSING
from pitchObjects.homeposition import HomePosition
from pitchObjects.pitchobject import PitchObject
import math

__author__ = 'Thomas'

class FieldPlayer(PitchObject):
    """Class for players currently on the pitch"""

    def __init__(self, playerRole, team, ball, posX, posY):
        """
        playerRole is a tuple (giving the percent position)
        """
        PitchObject.__init__(self, team.color, posX, posY, GRAPH_PLAYER_SIZE)

        self.homePosition = HomePosition(playerRole, team, ball)

        self.playerRole = playerRole
        self.team = team

        self.shootingRange = ATTR_SHOOTING_RANGE
        self.hasBall = False
        self.ball = ball
        self.isOffsides = False
        self.covering = []
        self.blocking = []
        self.marking = None
        self.isBlockedBy = []
        self.isCoveredBy = []
        self.recovering = 0 #If the player has recently lost the ball, they are recovering and cannot touch the ball
        self.chargeToBall = False
        self.speed = float(ATTR_PLAYER_SPEED)
        self.acceleration = float(ATTR_PLAYER_ACCEL)


    def isInShootingRange(self):
        if self.getWeightedDistanceToGoal(True) < self.shootingRange:
            return True
        else:
            return False

    def update(self, grandObserver):
        if self.recovering:
            self.recovering -= 1
        self.homePosition.update()
        self.makeAction(grandObserver)
        self.move()
        PitchObject.update(self)

    def accelerate(self, vectX, vectY):
        vectMag = math.sqrt(vectX**2 + vectY**2)
        if vectMag > 0:
            vectX = self.speed * vectX / vectMag
            vectY = self.speed * vectY / vectMag

            difX = (vectX - self.velX)
            difY = (vectY - self.velY)
            difMag = math.sqrt((vectX - self.velX)**2 + (vectY - self.velY)**2)
            if difMag > 0:
                self.velX += difX/difMag * self.acceleration
                self.velY += difY/difMag * self.acceleration


    def move(self):
        #Players can't move at the speed of rocket ships.
        if math.sqrt(self.velY**2 + self.velX**2) > self.speed:
            self.velX = self.speed * self.velX/math.sqrt(self.velY**2 + self.velX**2)
            self.velY = self.speed * self.velY/math.sqrt(self.velY**2 + self.velX**2)
        PitchObject.move(self)

    def makeAction(self, grandObserver):
        if self.team.hasPossession:
            if self.hasBall:
                self.makePlay(grandObserver)
            elif (self.ball.possessor is None) and self.chargeToBall:
                self.chase(self.ball)
            else:
                self.makeRun(grandObserver)
        else:
            self.defend()

    def makePlay(self, grandObserver):
        if self.ball.outOfPlay:
            self.cross()
        elif self.isInShootingRange():
            self.ball.simShot(self.team.isDefendingLeft)
        else:
            if not self.lookToPass(grandObserver):
                if self.getDistanceToGoalline(True) < STRAT_TRY_CROSSING:
                    self.cross()
                self.makeRun(grandObserver)

    def cross(self):
        teammates = sorted(self.team.players, key=lambda x: x.getWeightedDistanceToGoal(True))
        for player in teammates:
            if not player.blockedBy and not player.coveredBy and not player is self:
                self.ball.passTo(player)
                return
        self.ball.passTo(teammates[0])

    def lookToPass(self, grandObserver):
        if grandObserver.openPlayers:
            # TODO: introduce some intelligent randomness
            bestPassOption = self
            for openPlayer in grandObserver.openPlayers:
                if openPlayer is self:
                    break
                if math.sqrt((openPlayer.posY - self.posY)**2 + abs(openPlayer.posX - self.posX)**2) > STRAT_MIN_PASS:
                    bestPassOption = openPlayer
                    break
            if bestPassOption is not self:
                self.ball.passTo(bestPassOption)
                return True
        return False


    def makeRun(self, grandObserver):
        # TODO: make smarter runs and be more aggressive in front of goal
        if self.ball.outOfPlay is "Kickoff":
            pass
        elif grandObserver.lastDefender.getDistanceToGoalline(False) > self.getDistanceToGoalline(True) \
                < self.ball.getDistanceToGoalline(True, self.team.isDefendingLeft) and \
                        self.getDistanceToGoalline(True) < FIELD_LENGTH/2:
            self.accelerate( -self.dirX(1), 0)
        else:
            if self.ball.target is self:
                self.chase(self.ball)
            elif self.hasBall:
                self.accelerate( self.dirX(1), 0)
            else:
                self.chase(self.homePosition)


    def defend(self):
        if self.ball.outOfPlay:
            self.chase(self.homePosition)
        elif self.chargeToBall or self.nearBall():
            self.chase(self.ball)
        elif self.marking and self.getDistanceToGoalline(False) < 30 and \
                self.getDistanceToGoalline(False) < self.ball.getDistanceToGoalline(False, self.team.isDefendingLeft):
            self.accelerate(0, self.marking.posY - self.posY)
        elif self.marking:
            self.cover(self.marking)
        elif not pygame.sprite.collide_rect(self, self.homePosition):
            self.chase(self.homePosition)
        else:
            self.cover(self.ball)

    def nearBall(self):
        if self.squaredDistanceTo(self.ball) < STRAT_NEAR_BALL:
            return True
        else:
            return False

    def cover(self, pitchObject):
        if self.team.isDefendingLeft:
            object2goalvectX = 0 - pitchObject.posX
            self2goalvectX = 0 - self.posX

            #difX = pitchObject.posX - self.posX - 5
        else:
            object2goalvectX = FIELD_LENGTH - pitchObject.posX
            self2goalvectX = FIELD_LENGTH - self.posX
        object2goalvectY = FIELD_WIDTH/2 - pitchObject.posY
        self2goalvectY = FIELD_WIDTH/2 - self.posY

        object2goalMag = math.sqrt(object2goalvectX**2 + object2goalvectY**2)
        self2goalMag = math.sqrt(self2goalvectX**2 + self2goalvectY**2)

        objYnorm = object2goalvectY/object2goalMag
        objXnorm = object2goalvectX/object2goalMag
        selfYnorm = self2goalvectY/self2goalMag
        selfXnorm = self2goalvectX/self2goalMag

        if object2goalMag < self2goalMag:
            selfXnorm = selfXnorm * 2
            selfYnorm = selfYnorm * 2
        self.accelerate(selfXnorm - objXnorm, selfYnorm - objYnorm)

    def chase(self, pitchObject):
        # TODO: eventually want to factor in dervatives of position
        difX = pitchObject.posX - self.posX
        difY = pitchObject.posY - self.posY
        difMag = abs(difX) + abs(difY)
        if difMag > 0:
            self.accelerate(float(difX) / difMag, float(difY) / difMag)

    def getWeightedDistanceToGoal(self, attacking):
        return self.getDistanceToGoalline(attacking) + abs(self.posY - FIELD_WIDTH / 2) * 5/4

    def getDistanceToGoalline(self, attacking):
        return PitchObject.getDistanceToGoalline(self, attacking, self.team.isDefendingLeft)

    def dirX(self, horizontalValue):
        if self.team.isDefendingLeft:
            return horizontalValue
        else:
            return - horizontalValue
