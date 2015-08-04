from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import GRAPH_GOAL_SIZE, COLOR_GOAL
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'


class Goal(PitchObject):
    def __init__(self, leftGoal):
        if leftGoal:
            posX = - 1.5
        else:
            posX = FIELD_LENGTH + 1.5
        posY = FIELD_WIDTH/2
        PitchObject.__init__(self, COLOR_GOAL, posX, posY, GRAPH_GOAL_SIZE)
        PitchObject.update(self)

    def update(self):
        pass

    def move(self):
        pass