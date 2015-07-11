
__author__ = 'Thomas'

FIELD_LENGTH = 120 #this is horizontal dimension when displayed
FIELD_WIDTH = 80 #this is vertical dimension when displayed

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_HEADER_HEIGHT = WINDOW_HEIGHT-600

class DisplayMapper:
    def __init__(self):
        pass

def convertFieldPosition(posX,posY):
    dispX = int(posX * WINDOW_WIDTH/FIELD_LENGTH)
    dispY = int(posY * (WINDOW_HEIGHT-WINDOW_HEADER_HEIGHT)/FIELD_WIDTH)
    return (dispX,dispY)

def convertYards2Pixels(yards):
    pixels = yards * WINDOW_WIDTH/FIELD_LENGTH
    return pixels