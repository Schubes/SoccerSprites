from gamevariables import FIELD_LENGTH, FIELD_WIDTH, GAME_FPS
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

needsToBeImplemented = 10

class FieldPlayer(PitchObject):
    """Class for players currently on the pitch"""
    def __init__(self, playerRole, team, ball, pitchSurface, posX, posY):
        """
        playerRole is a string ("gk", "lb", "cb", etc...)
        """
        PitchObject.__init__(self, pitchSurface, team.color, posX, posY)
        self.playerRole = playerRole
        self.team = team
        self.shootingRange = needsToBeImplemented
        self.hasBall = False
        self.Ball = ball


    def getStartingPosX(self):
        #TODO: Choose where to put the players based on position
        return 0

    def getStartingPosY(self):
        #TODO: Choose where to put the players based on position
        return 0

    def isInShootingRange(self):
        if self.team.isDefendingLeft():
            if (self.posX + self.posY^2) < self.shootingRange:
                #I'm intentionally weighting the vertical distance stronger
                return True
        elif (self.posX-100 + self.posY^2) < self.shootingRange:
            return True

    def update(self):
        self.makeAction()
        PitchObject.update(self)

    def makeAction(self):
        if self.team.hasPossession:
            if self.hasBall == True:
                self.makePlay()
            else:
                self.makeRun()
        else:
            self.defend()

    def makePlay(self):
        if self.isInShootingRange():
            self.ball.simShot()
        else:
            #TODO: make this other sort of pass :P
            #TODO: let them dribble
            pass

    def makeRun(self):
        #TODO: Make players less stupid
        self.posX += float(needsToBeImplemented)/GAME_FPS
        self.confirmInBounds()


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

