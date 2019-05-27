import pygame

#Initialize pygame
pygame.init()

#This class creates a box body of a snake.
class SnakeBody:

    count = 0 #Keeps count of how many snakebody has been created

    #Default Contructor
    def __init__(self, XValue, YValue):
        self._XValue = XValue
        self._YValue = YValue
        self._Length = 60
        self._Height = 60

    # Getters
    @property
    def getXValue(self):
        return self._XValue

    @property
    def getYValue(self):
        return self._YValue

    @property
    def getLength(self):
        return self._Length

    @property
    def getHeight(self):
        return self._Height

    # Setter
    def setXValue(self, XValue):
        #make sure than it is within the boundary
        if XValue < 0:
            self._XValue = 800 #Here we are assuming 300 is the max x value   is 300
        elif XValue > 800:
            self._XValue = 0
        else:
            self._XValue = XValue

    def setYValue(self, YValue):

        #Make sure that the y value is within the boundary
        if YValue < 0:
            self._YValue = 800
        elif YValue > 800:
            self._YValue = 0
        else:
            YValue = YValue

    def toString(self):
        print("XValue: " + str(self._XValue) + " YValue: " + str(self._YValue))

