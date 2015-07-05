from gamevariables import FIELD_LENGTH, WINDOW_WIDTH, WINDOW_HEIGHT, FIELD_WIDTH, WINDOW_HEADER_HEIGHT

__author__ = 'Thomas'

class DisplayMapper:
    def __init__(self):
        pass

def convertFieldPosition(posX,posY):
    dispX = int(posX * WINDOW_WIDTH/FIELD_LENGTH)
    dispY = int(posY * (WINDOW_HEIGHT-WINDOW_HEADER_HEIGHT)/FIELD_WIDTH)
    return (dispX,dispY)