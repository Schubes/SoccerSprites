from gamevariables import FIELD_LENGTH, FIELD_WIDTH, COLOR_BALL
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self,pitchSurface):
        PitchObject.__init__(self,pitchSurface,COLOR_BALL)
        self.closetDefender = self.getClosetDefender()
        self.possesor = self.getPossesor()

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self):
        #TODO: make the players kick a bit harder
        self.posX = self.posX
        self.posY = self.posY

    def turnResult(self):
        pass

    def getClosetDefender(self):
        pass

    def getPossesor(self):
        pass