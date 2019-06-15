#First party imports
import threading
import time

# Third party imports
import pygame
import numpy as np

#Initialize pygame
pygame.init()

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
        self.snakeSpeedX = 10
        self.snakeSpeedY = 0
        self.direction = direction

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
            self._YValue = YValue

    def toString(self):
        print("XValue: " + str(self._XValue) + " YValue: " + str(self._YValue))

class Snake:

    count = 1
    def __init__(self, direction):
        self.A_Snake = [SnakeBody(350,350,direction)]

    #Add a body box to the snake's overall body.
    def addSnakeBox(self, direction):
        # Check the direction and add accordingly
        if direction == "right":
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue - 20,self.A_Snake[self.count - 1].getYValue , direction))
            print("right")
        elif direction == "left":
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue + 20, self.A_Snake[self.count - 1].getYValue, direction))
            print("left")

        elif direction == "up":
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue, self.A_Snake[self.count - 1].getYValue - 20, direction))
        elif direction == "down":
            self.A_Snake.append(SnakeBody(self.A_Snake[self.count - 1].getXValue,
                                          self.A_Snake[self.count - 1].getYValue + 20, direction))
        self.count += 1

    # Return the a specified snake body if it exists
    def getSnakeBox(self, indexNumber):
        return self.A_Snake[indexNumber]

    # Returns the count number.
    def getCountNumber(self):
        return self.count

    # Adjust the snake to keep it from leaving its form.
    def adjust(self, indexNumber):
        # Check the direction.
        if self.A_Snake[indexNumber].direction == "right":
            # It is to the right.
            # Make sure the the next snake body box is not empty.
            try:
                self.A_Snake[indexNumber + 1].setXValue(self.A_Snake[indexNumber].getXValue - 20)
                self.A_Snake[indexNumber + 1].setYValue(self.A_Snake[indexNumber].getYValue)
            except:
                print("")
        elif self.A_Snake[indexNumber].direction == "left":
            # It is to the left
            try:
                self.A_Snake[indexNumber + 1].setXValue(self.A_Snake[indexNumber].getXValue + 20)
                self.A_Snake[indexNumber + 1].setYValue(self.A_Snake[indexNumber].getYValue)
            except:
                print("")
        elif self.A_Snake[indexNumber].direction == "up":
            # It is up.
            try:
                self.A_Snake[indexNumber + 1].setXValue(self.A_Snake[indexNumber].getXValue)
                self.A_Snake[indexNumber + 1].setYValue(self.A_Snake[indexNumber].getYValue + 20)
            except:
                print("")
        elif self.A_Snake[indexNumber].direction == "down":
            # It is down
            try:
                self.A_Snake[indexNumber + 1].setXValue(self.A_Snake[indexNumber].getXValue)
                self.A_Snake[indexNumber + 1].setYValue(self.A_Snake[indexNumber].getYValue - 20)
            except:
                print("")

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
currentBoxNum = 0 # This is the current snake body number
isMoved = False
isAdded = False # If a box has been added
foodX = 0
foodY = 0
def paint():
    gameDisplay.fill((0,0,0))

    # Paint the food.
    global foodX
    global foodY
    pygame.draw.rect(gameDisplay, (0, 128, 255), (foodX, foodY, 20, 20))

    # Paint the snake on the canvas
    for counter in range(0, mainSnake.getCountNumber()):
        pygame.draw.rect(gameDisplay, (0, 128, 255), pygame.Rect(mainSnake.getSnakeBox(counter).getXValue,mainSnake.getSnakeBox(counter).getYValue, mainSnake.getSnakeBox(counter).getHeight, mainSnake.getSnakeBox(counter).getLength))
        #time.sleep(0.5)

    #Check for collisions with the food.
    for counter in range(0, mainSnake.getCountNumber()):
        if RectangleRectangleCollision(foodX, foodY, 20, 20, mainSnake.getSnakeBox(counter).getXValue, mainSnake.getSnakeBox(counter).getYValue, 20, 20):
            #Add a new box to the snake body.
            global isAdded # Indicate to the compiler that it is a global variable
            if isAdded == False:

                newDirection = mainSnake.getSnakeBox(mainSnake.getCountNumber() - 1).direction

                mainSnake.addSnakeBox(newDirection)
                threadSnake = threading.Thread(target=runSnake, args= (mainSnake.getCountNumber() - 1,))
                threadSnake.start()
                #isAdded = True
                foodX = np.random.randint(low=1, high=500)
                foodY = np.random.randint(low=1, high=500)


    pygame.display.flip()  #Update the screen
    time.sleep(0.0005)

#The game starts

#Begin by creating a snake.
mainSnake = Snake("right")

# Give default values for the snake speed.
SnakeX = 10
SnakeY = 0


# The following function will iterate through each snake body.
def iterateEachBody(direction):
    #Make sure that the current box number is 0.
    print("Start")

    for counter in range(0, mainSnake.getCountNumber()):
        print(counter)
        print(mainSnake.getSnakeBox(counter).getXValue)
        print(mainSnake.getSnakeBox(counter).getYValue)

        mainSnake.getSnakeBox(counter).snakeSpeedX = SnakeX
        mainSnake.getSnakeBox(counter).snakeSpeedY = SnakeY
        time.sleep(0.10)

        mainSnake.getSnakeBox(counter).direction = direction #adjust the direction
        mainSnake.adjust(counter) #adjust the snake

# The following function will deal with the snakes movements.
def runSnake(boxNum):

    # Local Variable List

    while(True):

        # Abjust X and Y values for the snake according to the current speed
        mainSnake.getSnakeBox(boxNum).setXValue(mainSnake.getSnakeBox(boxNum).getXValue + mainSnake.getSnakeBox(boxNum).snakeSpeedX )
        mainSnake.getSnakeBox(boxNum).setYValue(mainSnake.getSnakeBox(boxNum).getYValue + mainSnake.getSnakeBox(boxNum).snakeSpeedY )
        time.sleep(0.05)

#Make the snake run on a seperate thread.
threadSnake = threading.Thread(target = runSnake, args = (0,))
threadSnake.start()

#mainSnake.addSnakeBox("right")
#threadSnake = threading.Thread(target = runSnake, args = (1,))
#threadSnake.start()

#Next, create a random block.
foodX = np.random.randint(low = 1, high = 500)
foodY = np.random.randint(low = 1, high = 500)


#print(foodX)
#print(foodY)

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    #Repaint
    paint()

    #print("" + str(mainSnake.getSnakeBox(0).getYValue) + "  " + str(SnakeY)) #For testing/debugging purposes
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN:
        #The snake should move right
        if SnakeX != 10:
            SnakeX = 10
            SnakeY = 0

            # Make a seperate thread for the shifting movement
            threadMove = threading.Thread(target=iterateEachBody, args =("right",))
            threadMove.start()
            #print("" + str(SnakeX) + " " + str(SnakeY))
            currentBoxNum = 0


    elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_RIGHT:
        #The snake should move left
        if SnakeX != -10:
            SnakeX = -10
            SnakeY = 0
            # Make a seperate thread for the shifting movement
            threadMove = threading.Thread(target=iterateEachBody, args = ("left",))
            threadMove.start()

            #print("" + str(SnakeX) + " " + str(SnakeY))
            currentBoxNum = 0

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT :
        #The snake should move up
        if SnakeY != -10:
            SnakeY = -10
            SnakeX  = 0

            # Make a seperate thread for the shifting movement
            threadMove = threading.Thread(target=iterateEachBody, args = ("up",))
            threadMove.start()



            #print("" + str(SnakeX) + " " + str(SnakeY))
            currentBoxNum = 0


    elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not event.key == pygame.K_UP and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT:
        #The snake should move down
        if SnakeY != 10:
            SnakeY = 10
            SnakeX  = 0
            # Make a seperate thread for the shifting movement
            threadMove = threading.Thread(target=iterateEachBody, args = ("down",))
            threadMove.start()

            #print("" + str(SnakeX) + " " + str(SnakeY))
            currentBoxNum = 0
