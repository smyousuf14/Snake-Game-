#First party imports
import threading
import time

# Third party imports
import pygame
import numpy as np

#Initialize pygame
pygame.init()

# Declare global constants
DIRECTION_RIGHT = "right"
DIRECTION_LEFT = "left"
DIRECTION_UP = "up"
DIRECTION_DOWN = "down"

#This class creates a box body of a snake.
class SnakeBody:

    count = 0 #Keeps count of how many snakebody has been created

    #Default Contructor
    def __init__(self, XValue, YValue, direction):
        self._XValue = XValue
        self._YValue = YValue
        self._Length = 20
        self._Height = 20
        self.MAX_X = 500
        self.MAX_Y = 500
        self._direction = direction

        # Set the speed according to the direction
        if direction == DIRECTION_RIGHT:
            self._snakeSpeedX = 10
            self._snakeSpeedY = 0
        elif direction == DIRECTION_LEFT:
            self._snakeSpeedX = -10
            self._snakeSpeedY = 0
        elif direction == DIRECTION_UP:
            self._snakeSpeedX = 0
            self._snakeSpeedY = -10
        elif direction == DIRECTION_DOWN:
            self._snakeSpeedX = 0
            self._snakeSpeedY = 10


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

    @property
    def getSnakeSpeedX(self):
        return self._snakeSpeedX

    @property
    def getSnakeSpeedY(self):
        return self._snakeSpeedY

    @property
    def getDirection(self):
        return self._direction

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
            self._YValue = YValue

    def setDirection(self, direction):
        if direction == DIRECTION_RIGHT:
            self._snakeSpeedX = 10
            self._snakeSpeedY = 0
            self._direction = DIRECTION_RIGHT
        elif direction == DIRECTION_LEFT:
            self._snakeSpeedX = -10
            self._snakeSpeedY = 0
            self._direction = DIRECTION_LEFT
        elif direction == DIRECTION_UP:
            self._snakeSpeedX = 0
            self._snakeSpeedY = -10
            self._direction = DIRECTION_UP
        elif direction == DIRECTION_DOWN:
            self._snakeSpeedX = 0
            self._snakeSpeedY = 10
            self._direction = DIRECTION_DOWN

    def toString(self):
        print("XValue: " + str(self._XValue) + " YValue: " + str(self._YValue))
class Snake:

    count = 1
    def __init__(self, direction):
        self.A_Snake = [SnakeBody(350,350,direction)]

    #Add a body box to the snake's overall body.
    def addSnakeBox(self, direction):
        # Check the direction and add accordingly
        if direction == DIRECTION_RIGHT:
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue - 20,
                                          self.A_Snake[self.count - 1].getYValue , direction))

            #Adjust the speed such that it has the same speed as the block right before it.
            #self.A_Snake[self.count - 1].setDirection(self.A_Snake[self.count - 2].getDirection)
            #print(direction)
        elif direction == DIRECTION_LEFT:
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue + 20,
                                          self.A_Snake[self.count - 1].getYValue, direction))

            #Adjust the speed such that it has the same speed as the block right before it.
            #self.A_Snake[self.count - 1].setDirection(self.A_Snake[self.count - 2].getDirection)
            #print(direction)

        elif direction == DIRECTION_UP:
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue,
                                          self.A_Snake[self.count - 1].getYValue + 20, direction))
            #print(direction)
            # Adjust the speed such that it has the same speed as the block right before it.
            #self.A_Snake[self.count - 1].setDirection(self.A_Snake[self.count - 2].getDirection)
        elif direction == DIRECTION_DOWN:
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue,
                                          self.A_Snake[self.count - 1].getYValue - 20, direction))
            #print(direction)
            # Adjust the speed such that it has the same speed as the block right before it.
            #self.A_Snake[self.count - 1].setDirection(self.A_Snake[self.count - 2].getDirection)

        self.count += 1
        #print(self.count)

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
pressedDown = False
currentBoxNum = 0 # This is the current snake body number
foodX = 0
foodY = 0

def paint():
    gameDisplay.fill((0,0,0))

    # Paint the food.
    global foodX
    global foodY
    pygame.draw.rect(gameDisplay, (0, 128, 255), (foodX, foodY, 20, 20))

    #move
    runSnake()

    # Paint the snake on the canvas
    for counter in range(0, mainSnake.getCountNumber()):
        pygame.draw.rect(gameDisplay, (0, 128, 255), pygame.Rect(mainSnake.getSnakeBox(counter).getXValue,mainSnake.getSnakeBox(counter).getYValue, mainSnake.getSnakeBox(counter).getHeight, mainSnake.getSnakeBox(counter).getLength))



    # Check for collisions with the food.
    for counter in range(0, mainSnake.getCountNumber()):
        if RectangleRectangleCollision(foodX, foodY, 20, 20, mainSnake.getSnakeBox(counter).getXValue,
                                       mainSnake.getSnakeBox(counter).getYValue, 20, 20):

            # Add a new box to the snake body.
            newDirection = mainSnake.getSnakeBox(mainSnake.getCountNumber() - 1).getDirection
            print(mainSnake.getCountNumber()) #For Debugging
            mainSnake.addSnakeBox(newDirection)

            foodX = np.random.randint(low=1, high=500)
            foodY = np.random.randint(low=1, high=500)

    # Check for collisions of the head with any part of the snake.
    for indexNumber in range(1, mainSnake.getCountNumber()):
        if RectangleRectangleCollision(mainSnake.getSnakeBox(0).getXValue, mainSnake.getSnakeBox(0).getYValue, 20, 20,
                                       mainSnake.getSnakeBox(indexNumber).getXValue, mainSnake.getSnakeBox(indexNumber).getYValue, 20, 20):
            # End the game.
            global isRunning
            #isRunning = False

    pygame.display.flip()  # Update the screen

    time.sleep(0.10)
#The game starts

#Begin by creating a snake.
mainSnake = Snake(DIRECTION_RIGHT)

# The following function will deal with the snakes movements.
def runSnake():

    for indexNumber in range(0, mainSnake.getCountNumber()):

        mainSnake.getSnakeBox(indexNumber).setXValue(
            mainSnake.getSnakeBox(indexNumber).getXValue + mainSnake.getSnakeBox(indexNumber).getSnakeSpeedX)

        mainSnake.getSnakeBox(indexNumber).setYValue(
            mainSnake.getSnakeBox(indexNumber).getYValue + mainSnake.getSnakeBox(indexNumber).getSnakeSpeedY)

    # wait a while
    #time.sleep(0.10)

# Iterate this direction through each box in the snake body.
def iterateEachBody(direction):

    snakeLimit = mainSnake.getCountNumber()

    #Create isAdded
    isAdded = False

    for indexNumber in range(0, snakeLimit):

        mainSnake.getSnakeBox(indexNumber).setDirection(direction)

        if snakeLimit != mainSnake.getCountNumber():
            isAdded = True

        #Delay for a certain time.
        time.sleep(0.20)

    if snakeLimit != mainSnake.getCountNumber():
        isAdded = True


    if isAdded:
        mainSnake.getSnakeBox(mainSnake.getCountNumber() - 1).setDirection(direction)
        isAdded = False


# Start running the movements of the snake in a sepearate thread
#threadSnake = threading.Thread(target = runSnake)
#threadSnake.start()

#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)

#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)

#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)

#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)
#mainSnake.addSnakeBox(DIRECTION_RIGHT)


#Next, create a random block.
foodX = np.random.randint(low = 1, high = 500)
foodY = np.random.randint(low = 1, high = 500)

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    #Repaint
    paint()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN:
        #The snake should move right
        if mainSnake.getSnakeBox(0).getDirection != DIRECTION_RIGHT:
            runningThread = threading.Thread(target = iterateEachBody, args = (DIRECTION_RIGHT,))
            runningThread.start()

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_RIGHT:
        #The snake should move left
        if mainSnake.getSnakeBox(0).getXValue != DIRECTION_LEFT:
            runningThread = threading.Thread(target=iterateEachBody, args = (DIRECTION_LEFT,))
            runningThread.start()

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT :
        #The snake should move up
        if mainSnake.getSnakeBox(0).getYValue != DIRECTION_UP:
            runningThread = threading.Thread(target=iterateEachBody, args = (DIRECTION_UP,))
            runningThread.start()

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not event.key == pygame.K_UP and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT:
        #The snake should move down
        if mainSnake.getSnakeBox(0).getYValue != DIRECTION_DOWN:
            runningThread = threading.Thread(target=iterateEachBody, args = (DIRECTION_DOWN,))
            runningThread.start()
