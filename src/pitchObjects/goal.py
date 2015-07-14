from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GRAPH_GOAL_SIZE

__author__ = 'Thomas'


class Goal(PitchObject):
    def __init__(self, rightGoal):
        if rightGoal:
            posX = FIELD_LENGTH
        else:
            posX = 0
        posY = FIELD_WIDTH/2
        PitchObject.__init__(self, COLOR_BALL, posX, posY, GRAPH_GOAL_SIZE)