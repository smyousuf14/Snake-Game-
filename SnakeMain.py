#First party imports
import threading
import time

# Third party imports
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

    count = 1
    def __init__(self):
        self.A_Snake = [SnakeBody(350,350)]

    #Add a body box to the snake's overall body.
    def addSnakeBox(self):
        self.A_Snake.append(SnakeBody(350 + (self.count * 20),350))
        self.count += 1

    # Return the a specified snake body if it exists
    def getSnakeBox(self, indexNumber):
        return self.A_Snake[indexNumber]

    # Returns the count number.
    def getCountNumber(self):
        return self.count

# Determine if there is a collision between two rectangle objects.
def RectangleRectangleCollision(x1,y1,l1,h1, x2,y2,l2,h2):
    isCollision = False

    #Check Top left
    if x1 <= (x2 + l2) and x1 >= (x2):

        if y1 >= y2 and y1 <= (y2 + h2):
            isCollision = True

    # Check top right
    if (x1 + l1)<= (x2 + l2) and (x1 + l1) >= (x2):

        if y1  >= y2 and y1 <= (y2 + h2):
            isCollision = True

    # Check bottom left
    if x1 <= (x2 + l2) and x1 >= (x2):
        if (y1 + h1) >= y2 and (y1 + h1) <= (y2 + h2):
            isCollision = True

    # Check bottom right
    if (x1 + l1) <= (x2 + l2) and (x1 + l1) >= (x2):
        if (y1 + h1) >= y2 and (y1 + h1) <= (y2 + h2):
            isCollision = True

    return isCollision
#----------------------Main Game--------------------------------------------------

#Create a display
gameDisplay = pygame.display.set_mode((500,500))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

#Global Variables
isRunning = True
RecX  = 30
RecY = 30
int = 0
pressedDown = False

def paint():
    gameDisplay.fill((0,0,0))

    # Paint the snake on the canvas
    for counter in range(0, mainSnake.getCountNumber()):
        pygame.draw.rect(gameDisplay, (0, 128, 255), pygame.Rect(mainSnake.getSnakeBox(counter).getXValue,mainSnake.getSnakeBox(counter).getYValue, 20, 20))

    pygame.display.flip()  #Update the screen
    clock.tick(100)

#The game starts

#Begin by creating a snake.
mainSnake = Snake()

# Give default values for the snake speed.
SnakeX = 1
SnakeY = 0

# The following function will deal with the snakes movements.
def runSnake():
    while(True):

        # Abjust X and Y values for the snake according to the current speed
        for counter in range(0, mainSnake.getCountNumber()):
            mainSnake.getSnakeBox(counter).setXValue(mainSnake.getSnakeBox(counter).getXValue + SnakeX)
            mainSnake.getSnakeBox(counter).setYValue(mainSnake.getSnakeBox(counter).getYValue + SnakeY)
        time.sleep(4)

while isRunning:

    #Make the snake run on a seperate thread.
    threadSnake = threading.Thread(target = runSnake)
    threadSnake.start()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        #Repaint
        paint()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #The snake should move right
            paint()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #The snake should move left
            paint()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #The snake should move up
            paint()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #The snake should move down
            paint()
