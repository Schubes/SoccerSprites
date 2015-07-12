import pygame
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import STRAT_NEAR_BALL, ATTR_PLAYER_SPEED, ATTR_SHOOTING_RANGE, GRAPH_PLAYER_SIZE, ATTR_PLAYER_ACCEL, \
    STRAT_MIN_PASS
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
        self.isClosestToBall = False
        self.speed = float(ATTR_PLAYER_SPEED)
        self.acceleration = ATTR_PLAYER_ACCEL

    def isInShootingRange(self):
        if self.getWeightedDistanceToGoal(True) < self.shootingRange:
            return True
        else:
            return False

    def update(self, grandObserver):
        self.homePosition.update()
        self.makeAction(grandObserver)
        # self.move()
        self.confirmInBounds()
        PitchObject.update(self)

    def makeAction(self, grandObserver):
        if self.team.hasPossession:
            if self.hasBall:
                self.makePlay(grandObserver)
            else:
                self.makeRun(grandObserver)
        else:
            self.defend()

    def makePlay(self, grandObserver):
        if self.isInShootingRange():
            self.ball.simShot(self.team.isDefendingLeft)
        else:
            if grandObserver.openPlayers:
                print len(grandObserver.openPlayers)
                #this works because openPlayers is sorted by closeness to opponent's goal
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
                else:
                    self.makeRun(grandObserver)
            else:
                self.makeRun(grandObserver)

    def makeRun(self, grandObserver):
        if self.isOffsides:
            self.posX -= self.dirX(self.speed)
        else:
            if self.ball.target is self:
                self.chase(self.ball)
            elif self.hasBall:
                self.posX += self.dirX(self.speed)
            elif self.ball.isLoose and pygame.sprite.collide_rect(self, self.homePosition):
                self.chase(self.ball)
            else:
                self.chase(self.homePosition)


    def defend(self):
        if self.isClosestToBall or self.nearBall():
            self.chase(self.ball)
        elif self.marking and self.getDistanceToGoalline(False) < 30:
            pass
        elif self.marking:
            self.cover(self.marking)
        elif self.marking:
            self.chase(self.marking)
        elif not pygame.sprite.collide_rect(self, self.homePosition):
            self.chase(self.homePosition)
        elif self.getDistanceToGoalline(False) > 30:
            self.cover(self.ball)
        else:
            self.chase(self.ball)

    def nearBall(self):
        if self.squaredDistanceTo(self.ball) < STRAT_NEAR_BALL:
            return True
        else:
            return False

    def cover(self, pitchObject):
        if self.team.isDefendingLeft:
            difX = pitchObject.posX - self.posX - 5
        else:
            difX = pitchObject.posX - self.posX + 5
        difY = pitchObject.posY - self.posY
        dif = abs(difX) + abs(difY)
        if not dif == 0:
            self.posX += float(difX) / dif * self.speed
            self.posY += float(difY) / dif * self.speed

    def chase(self, pitchObject):
        # TODO: eventually want to factor in dervatives of position
        difX = pitchObject.posX - self.posX
        difY = pitchObject.posY - self.posY
        dif = abs(difX) + abs(difY)
        if not dif == 0:
            self.posX += float(difX) / dif * self.speed
            self.posY += float(difY) / dif * self.speed

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
        return self.getDistanceToGoalline(attacking) + abs(self.posY - FIELD_WIDTH / 2) * 2

    def getDistanceToGoalline(self, attacking):
        return PitchObject.getDistanceToGoalline(self, attacking, self.team.isDefendingLeft)

    def dirX(self, horizontalValue):
        if self.team.isDefendingLeft:
            return horizontalValue
        else:
            return - horizontalValue
