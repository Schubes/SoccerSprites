import math
from abc import ABCMeta, abstractmethod
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import STRAT_NEAR_BALL, ATTR_SHOOTING_RANGE, ATTR_PLAYER_SPEED, ATTR_PLAYER_ACCEL, STRAT_MIN_PASS
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'



class AbstractPlayer(PitchObject):
    """Abstract Class that contains the fundamentals for player movement.
    Children classes should implement the logic to determine which action the player should take
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, color, posX, posY, size):

        self.shootingRange = ATTR_SHOOTING_RANGE
        self.hasBall = False
        self.isOffsides = False
        self.covering = []
        self.blocking = []
        self.marking = None
        self.blockedBy = []
        self.coveredBy = []

        self.recovering = 0 #If the player has recently lost the ball, they are recovering and cannot touch the ball

        self.chargeToBall = False
        self.maxSpeed = float(ATTR_PLAYER_SPEED)
        self.acceleration = float(ATTR_PLAYER_ACCEL)

        PitchObject.__init__(self, color, posX, posY, size)

    def makeAction(self, grandObserver):
        raise NotImplementedError()

    def makeAction(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        if self.recovering:
            self.recovering -= 1
        self.move()
        PitchObject.update(self)

    def chase(self, pitchObject, posY = None):
        """ If one param is passed, chases that pitchObject.
        If two params (posX and posY) are passed chases that location.
        """
        if posY:
            posX = pitchObject
        else:
            posX = pitchObject.posX
            posY = pitchObject.posY

        difX = posX - self.posX
        difY = posY - self.posY
        difMag = abs(difX) + abs(difY)
        if difMag > 0:
            self.accelerate(float(difX) / difMag, float(difY) / difMag)

    def coverObject(self, pitchObject):
        """ If the player is between the goal and the pitchObject, returns True
        Otherwise, moves the player in between the pitchObject and the goal, returns False
        """
        if self.team.isDefendingLeft:
            object2goalvectX = 0 - pitchObject.posX
            self2goalvectX = 0 - self.posX
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

        # if the object is closer to the goal, we need to make our player run back to the goal.
        if object2goalMag < self2goalMag:
            selfXnorm = selfXnorm * 2
            selfYnorm = selfYnorm * 2

        difX = (selfXnorm - objXnorm)
        difY = (selfYnorm - objYnorm)
        # print difX**2 + difY**2
        if (difX**2 + difY**2) > .01:
            self.accelerate(difX, difY)
            return True
        return False


    def accelerate(self, vectX, vectY):
        """ This method changes the direction of the player to match the input vector as quickly as possible.
        This method should only be called once per update call.
        """
        if not self.ball.outOfPlay:
            if self.velY + self.posY > FIELD_WIDTH:
                if vectY > 0:
                    vectY = 0
            elif self.velY + self.posY < 0:
                if vectY < 0:
                    vectY = 0
            if self.velX + self.posX > FIELD_LENGTH:
                if vectX > 0:
                    vectX = 0
            elif self.velX + self.posX < 0:
                if vectX < 0:
                    vectX = 0

        vectMag = math.sqrt(vectX**2 + vectY**2)
        if vectMag > 0:
            vectX = self.maxSpeed * vectX / vectMag
            vectY = self.maxSpeed * vectY / vectMag
        else:
            vectX = 0
            vectY = 0

        difX = (vectX - self.velX)
        difY = (vectY - self.velY)
        difMag = math.sqrt((vectX - self.velX)**2 + (vectY - self.velY)**2)
        if difMag > 0:
            self.velX += float(difX)/difMag * self.acceleration
            self.velY += float(difY)/difMag * self.acceleration

    def move(self):
        """
        Ensures the player does not move faster the its maximum speed and updates the player position
        """
        # if self.hasBall:
        #     if math.sqrt(self.velY**2 + self.velX**2) > (float(4)/5 * self.maxSpeed):
        #         self.velX = float(4)/5 * self.maxSpeed * self.velX/math.sqrt(self.velY**2 + self.velX**2)
        #         self.velY = float(4)/5 * self.maxSpeed * self.velY/math.sqrt(self.velY**2 + self.velX**2)
        if math.sqrt(self.velY**2 + self.velX**2) > self.maxSpeed:
            self.velX = self.maxSpeed * self.velX/math.sqrt(self.velY**2 + self.velX**2)
            self.velY = self.maxSpeed * self.velY/math.sqrt(self.velY**2 + self.velX**2)
        PitchObject.move(self)

    def intercept(self, pitchObject):
        """ This method is primarily used to recieve passes, moves the player to a point where the pitchObject will
        arrive, or if the object is not moving chases it.
        """
        objectSpeed = math.sqrt(pitchObject.velX**2 + pitchObject.velY**2)
        if objectSpeed > 0:
            objXnorm = pitchObject.velX/objectSpeed
            objYnorm = pitchObject.velY/objectSpeed

            selfvectX = pitchObject.velX*100000000 + pitchObject.posX - self.posX
            selfvectY = pitchObject.velY*100000000 + pitchObject.posY - self.posY

            selfMag = math.sqrt(selfvectX**2 + selfvectY**2)

            if selfMag > 0:
                difX = selfvectX/selfMag - objXnorm
                difY = selfvectY/selfMag - objYnorm
                difMag = math.sqrt(difX**2 + difY**2)
                if difMag > 5e-10:
                    self.accelerate(float(difX) / difMag, float(difY) / difMag)
                else:
                    self.accelerate(0,0)
        else:
            self.chase(pitchObject)

    def lookToPass(self, grandObserver):
        """

        :param grandObserver:
        :return: Boolean (if good pass was found)
        """
        if grandObserver.openPlayers:
            bestPassOption = self
            secondWorstPassOption = None
            worstPassOption = None
            for openPlayer in grandObserver.openPlayers:
                if not openPlayer.recovering:
                    if openPlayer is self.ball.prevPossessor:
                        secondWorstPassOption = openPlayer
                    elif openPlayer is self:
                        break
                    elif math.sqrt((openPlayer.posY - self.posY)**2 + abs(openPlayer.posX - self.posX)**2) > STRAT_MIN_PASS:
                        bestPassOption = openPlayer
                        break
            if bestPassOption is not self:
                self.ball.passTo(bestPassOption, True)
                return True
            elif secondWorstPassOption:
                self.ball.passTo(secondWorstPassOption, True)
                return True
            elif worstPassOption:
                print "and it's played back"
                self.ball.passTo(worstPassOption, True)
                return True
        return False

    def mustPass(self):
        """
        For situations where a pass is required, eg. throwins
        """
        teammates = sorted(self.team.players, key=lambda x: x.getWeightedDistanceToGoal(True))
        for player in teammates:
            if not player.blockedBy and not player.coveredBy and not player is self:
                self.ball.passTo(player, False)
                return
        self.ball.passTo(teammates[0],False)

    def returnOnsides(self, grandObserver):
        if self.team.hasPossession:
            if grandObserver.lastDefender.getDistanceToGoalline(False) > self.getDistanceToGoalline(True) \
                < self.ball.getDistanceToGoalline(True, self.team.isDefendingLeft) and \
                self.getDistanceToGoalline(True) < FIELD_LENGTH/2:
                self.accelerate( -self.dirX(1), 0)
                return True
        else:
            if grandObserver.lastAttacker.getDistanceToGoalline(True) > self.getDistanceToGoalline(True) \
                    < self.ball.getDistanceToGoalline(True, self.team.isDefendingLeft) and \
                            self.getDistanceToGoalline(True) < FIELD_LENGTH/2:
                self.accelerate( -self.dirX(1), 0)
                return True
        return False

    def nearBall(self):
        if self.getDistanceTo(self.ball) < STRAT_NEAR_BALL:
            return True
        else:
            return False

    def isInShootingRange(self):
        if self.getWeightedDistanceToGoal(True) < self.shootingRange:
            return True
        else:
            return False

    def getWeightedDistanceToGoal(self, attacking):
        return self.getDistanceToGoalline(attacking) + abs(self.posY - FIELD_WIDTH / 2) * 5/4

    def getDistanceToGoalline(self, attacking):
        return PitchObject.getDistanceToGoalline(self, attacking, self.team.isDefendingLeft)

    def dirX(self, horizontalValue):
        if self.team.isDefendingLeft:
            return horizontalValue
        else:
            return - horizontalValue