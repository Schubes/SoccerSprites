"""
This file holds the variables and class to handle the mapping between yards and the pixels. This allows the match logic
to be computed in the more comfortable unit of yards and be properly displayed on whatever the current window size is.
"""

__author__ = 'Thomas'

FIELD_LENGTH = 120 #this is horizontal dimension when displayed
FIELD_WIDTH = 80 #this is vertical dimension when displayed

WINDOW_WIDTH = 950
WINDOW_HEIGHT = 750
WINDOW_HEADER_HEIGHT = 100
WINDOW_BORDER = 25

class DisplayMapper:
    def __init__(self):
        pass

def convertFieldPosition(posX,posY):
    dispX = int(posX * (WINDOW_WIDTH - (WINDOW_BORDER * 2))/FIELD_LENGTH) + WINDOW_BORDER
    dispY = int(posY * (WINDOW_HEIGHT - (WINDOW_HEADER_HEIGHT + (WINDOW_BORDER * 2)))/FIELD_WIDTH) + WINDOW_BORDER
    return (dispX,dispY)

def convertYards2Pixels(yards):
    pixels = yards * WINDOW_WIDTH/FIELD_LENGTH
    return pixels