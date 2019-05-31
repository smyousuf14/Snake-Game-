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
        self.MAX_X = 800
        self.MAX_Y = 800

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
            self._XValue = self.MAX_X  + XValue
        elif XValue > self.MAX_X:
            self._XValue = 0 + (XValue - self.MAX_X)
        else:
            self._XValue = XValue

    def setYValue(self, YValue):

        #Make sure that the y value is within the boundary
        if YValue < 0:
            self._YValue = self.MAX_Y + YValue
        elif YValue > self.MAX_Y:
            self._YValue = 0 + (YValue - self.MAX_Y)
        else:
            YValue = YValue

    def toString(self):
        print("XValue: " + str(self._XValue) + " YValue: " + str(self._YValue))

class Snake:

    def __init__(self):
        self.A_Snake = [SnakeBody(350,350)]

    #Add a body box to the snake's overall body.
    def addSnakeBox(self):
        self.A_Snake.append(SnakeBody(350,350))

    # Return the a specified snake body if it exists
    def getSnakeBox(self, indexNumber):
        return self.A_Snake[indexNumber]

S1 = Snake()
S1.getSnakeBox(0).toString()
S1.addSnakeBox()
S1.getSnakeBox(1).toString()
