import pygame
from random import randint
from time import sleep

pygame.init()

### DEFINING THE ESSENTIALS ###

fps = 50  # frames per second (standard: 50)
display_x = 1000  # screen width in pixel (standard: 800)
display_y = 600  # screen hight in pixel (standard: 600)

# graphics layers for the display
forestLayer = 0
bgdLayer = 1
monkeyLayer = 2
obstLayer = 3
fgdLayer = 4
textLayer = 5

maxSpeed = 15  # maximum speed in x-direction
speedTot = 12  # total speed for jump hight (maxSpeed < speedTot)

# postion of monkey
x0 = int(display_x * 0.1)
y0 = int(display_y * 0.85)

mainFont = pygame.font.Font('Kirang Haerang regular.ttf', 50)
bigFont = pygame.font.Font('Kirang Haerang regular.ttf', 120)
white = (255, 255, 255)
red = (255, 0, 0)

### LOADING ALL IMAGE FILES ###

forestFiles = ['forest1.png', 'forest2.png', 'forest3.png',
    'forest4.png', 'forest5.png', 'forest6.png', 'forest7.png']
backgroundFiles = ['background1.png', 'background2.png', 'background3.png',
    'background4.png']
foregroundFiles = ['foreground1.png', 'foreground2.png', 'foreground3.png',
    'foreground4.png']
obstacleFiles = ['obstacle1.png', 'obstacle2.png']

forestObject = [pygame.image.load('MonkeyGIF/' + item) for item in forestFiles]
backgroundObject = [pygame.image.load('MonkeyGIF/' + item) for item in backgroundFiles]
foregroundObject = [pygame.image.load('MonkeyGIF/' + item) for item in foregroundFiles]
obstacleObject = [pygame.image.load('MonkeyGIF/' + item) for item in obstacleFiles]
allObjects = [forestObject, backgroundObject, foregroundObject, obstacleObject]

carImages = [pygame.image.load('MonkeyGIF/movingObstacle' + str(im + 1) + '.png') for
    im in range(1)]
movingObjects = [carImages]

floorImage = pygame.image.load('MonkeyGIF/Floor.png')
floorWidth = floorImage.get_rect()[2]

monkeyImages = [pygame.image.load('MonkeyGIF/monkeyColor' + str(im + 1) + '.png') for
    im in range(8)]
monkeyImages2 = [pygame.image.load('MonkeyGIF/monkeyThumbColor' + str(im + 1) + '.png') for
    im in range(8)]
monkeyImages3 = pygame.image.load('MonkeyGIF/monkeyJump.png')
allMonkeys = [monkeyImages, monkeyImages2, monkeyImages3]

### FUNCTIONS AND CLASSES ###
        
def initObject(what, lastX):
    if what == 0:  # forest
        xMin, xMax = 20, 50
        yMin, yMax = int(display_y * 0.68), int(display_y * 0.7)
        imNo = randint(0, len(forestObject) - 1)
    elif what == 1:  # background
        xMin, xMax = int(display_x * 0.3), int(display_x * 0.6)
        yMin, yMax = int(display_y * 0.74), int(display_y * 0.8)
        imNo = randint(0, len(backgroundObject) - 1)
    elif what == 2:  # foreground
        xMin, xMax = int(display_x * 0.9), int(display_x * 1.8)
        yMin, yMax = int(display_y * 0.95), int(display_y * 0.99)
        imNo = randint(0, len(foregroundObject) - 1)
    elif what == 3:  # obstacle
        xMin, xMax = int(display_x * 1), int(display_x * 1.5)
        yMin, yMax = int(display_y * 0.899), int(display_y * 0.9)
        imNo = randint(0, len(obstacleObject) - 1)
    
    xPos = lastX + randint(xMin, xMax)
    yPos = randint(yMin, yMax)
    return xPos, yPos, imNo

   
# rotates the input image by angle. The resulting rect has different dimensions.
# which is compensated by shifting the image by (offX, offY)   
def rotateImage(image, angle):
    center = image.get_rect().center
    imageRot = pygame.transform.rotate(image, -angle)
    centerRot = imageRot.get_rect().center
    offX, offY = center[0] - centerRot[0], center[1] - centerRot[1]
    return imageRot, offX, offY
    

# this function displays the rect() of an image
# this can be used for checking out hitboxes for collisions! 
def rectAround(image, xpos, ypos):
    rect = image.get_rect()
    xpos = int(xpos)
    ypos = int(ypos)
    rect[0] = xpos
    rect[1] = ypos
    width = rect[2]
    hight = rect[3]
    pygame.draw.rect(gameDisplay, white, rect, 1)
    pygame.draw.circle(gameDisplay, red, (xpos, ypos), 3)
    pygame.draw.circle(gameDisplay, white, (xpos + width, ypos), 3)
    pygame.draw.circle(gameDisplay, white, (xpos, ypos + hight), 3)
    pygame.draw.circle(gameDisplay, white, (xpos + width, ypos + hight), 3)


class avatar:
    
    jumpOffset = 40
    
    def __init__(self, what):
        self.what = what
        self.counter = 0
        self.layer = monkeyLayer
        self.jumping = False
        self.jumpY = 0.
        self.jumpTime = 0.
        self.maxTime = 0.
        self.image = 0.
        self.hight = allMonkeys[self.what][0].get_rect()[3]
        self.width = allMonkeys[self.what][0].get_rect()[2]
        self.hightRot = self.hight
        self.widthRot = self.width
        self.xpos, self.ypos = x0, y0 - self.hight
    
    def display(self, speed):
        
        # if the monkey is JUMPING show the rotating image
        if self.jumping == True:
            self.jumpTime += 1. / fps
            self.jumpY = (-5. * self.jumpTime**2 + (speedTot + speed/1.5) * self.jumpTime) * 70
            if -speed < 4:
                turns = 3
            elif -speed < 8:
                turns = 2
            else:
                turns = 1
            angle = 360 * turns * self.jumpTime / self.maxTime
            self.imageData, offX, offY = rotateImage(allMonkeys[self.what], angle)
            self.xpos = x0 + offX
            self.ypos = y0 - self.jumpY - self.jumpOffset - self.hight + offY
        # if the monkey in RUNNING show the sequence of pictures (8 pictures)
        else:
            self.jumpY = 0.
            self.counter += -speed
            self.image = int(self.counter / fps * 2) & 7
            self.imageData = allMonkeys[self.what][self.image]
            offX, offY = 0, 0
        
        rect = self.imageData.get_rect()
        self.hightRot = rect[3]
        self.widthRot = rect[2]
        gameDisplay.blit(self.imageData, (self.xpos, self.ypos))
        rectAround(self.imageData, self.xpos, self.ypos)
            
        if self.what == 2 and self.jumpTime > self.maxTime:
            global jumpOn
            jumpOn = False
            self.xpos = x0
            self.ypos = y0 - self.hight
            self.jumping = False
            self.what = 1
            self.counter = 0
            
        if self.what == 1 and self.counter / fps > 2:
            self.what = 0
            
    def startJump(self, speed):
        self.jumping = True
        self.what = 2
        self.jumpTime = 0.
        self.maxTime = 0.2 * (speedTot - speed/1.5)


class movingObstacle:
    
    def __init__(self, which, velocity):
        self.what = 3
        self.which = which
        self.velocity = velocity
        self.layer = obstLayer
        self.hight = movingObjects[which][0].get_rect()[3]
        self.width = movingObjects[which][0].get_rect()[2]
        self.xpos, self.ypos, dummy = initObject(3, canvasElement.largestX[3])
        self.ypos = self.ypos - self.hight
        canvasElement.largestX[3] = self.xpos
        self.image = 0
        
    def display(self, speed):
        self.xpos += -self.velocity + speed * canvasElement.relativeSpeed[3]
        self.imageData = movingObjects[self.which][self.image]
        gameDisplay.blit(self.imageData, (self.xpos, self.ypos))
        rectAround(self.imageData, self.xpos, self.ypos)

class canvasElement:
    
    # the following lists are sorted as [forest, backg., foreg., obstacle]
    largestX = [0, 0, 0, 0]  # x-position of last object
    relativeSpeed = [0.5, 0.75, 1, 0.85]  # relative moving speed of objects
    layers = [forestLayer, bgdLayer, fgdLayer, obstLayer] # layer for display

    def __init__(self, what):
        self.what = what
        self.xpos, self.ypos, self.image = initObject(what, self.largestX[what])
        canvasElement.largestX[what] = self.xpos
        self.hight = allObjects[self.what][self.image].get_rect()[3]
        self.width = allObjects[self.what][self.image].get_rect()[2]
        self.ypos = self.ypos - self.hight
        self.layer = self.layers[what]

    def display(self, speed):
        self.xpos += speed * self.relativeSpeed[self.what]
        self.imageData = allObjects[self.what][self.image]
        gameDisplay.blit(self.imageData, (self.xpos, self.ypos))
        if self.what == 3:
            rectAround(self.imageData, self.xpos, self.ypos)

    @classmethod
    def updateLargestX(cls, speed):
        cls.largestX = [elem + speed * cls.relativeSpeed[item] 
            for item, elem in enumerate(cls.largestX)]
        
        
class messageText:
    
    def __init__(self, text, font, color, xpos, ypos, numbers = False, alignment = 0):
        self.what = -1
        self.layer = textLayer
        self.text = text
        self.numbers = numbers
        self.value = 0
        self.font = font
        self.color = color
        self.xpos = xpos
        self.ypos = ypos
        self.width = 0
        self.alignment = alignment
        
    def display(self, speed = None):
        if self.numbers:
            text = self.font.render(self.text + str(int(self.value)), True, self.color)
        else:
            text = self.font.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.xpos, self.ypos)
        if self.alignment == -1:
            textRect.left = self.xpos
        if self.alignment == 1:
            textRect.right = self.xpos
        
        gameDisplay.blit(text, textRect)

        
def fillScreen(displayElements, xMax):
    while canvasElement.largestX[0] < xMax:  # adds forest elements
        displayElements.append(canvasElement(0))
    while canvasElement.largestX[1] < xMax:  # adds background elements
        displayElements.append(canvasElement(1))
    while canvasElement.largestX[2] < xMax:  # adds foreground elements
        displayElements.append(canvasElement(2))
    while canvasElement.largestX[3] < 0:  # adds obstacles
        if randint(0, 9) < 5:
            displayElements.append(canvasElement(3))
        else:
            displayElements.append(movingObstacle(0, maxSpeed))
    return displayElements
    
    
def firstPixel(image, pos, step, depth, direction):
    rect = image.get_rect()
    if direction == 0:  # from the left
        first = 0
        last = depth - 1
        index = 0
    elif direction == 1:  # from the right
        first = depth - 1
        last = 0
        index = 0
        step = -step
    elif direction == 2:  # from the top
        first = 0
        last = depth - 1
        index = 1
    elif direction == 3:  # from the bottom
        first = depth - 1
        last = 0
        index = 1
        step = -step
    pos = [pos, pos]
    check1 = first
    check2 = first
    if depth > rect[index+2] or depth < 1 or pos[0] < 0 or pos[0] > rect[3-index]-1:
        print('error:', pos, rect, check1, direction, last, depth, index)
        return -1
    while True:  # search with a fixed step size
        pos[index] = check2
        if image.get_at(tuple(pos))[3] != 0:
            break  # pixel with alpha != 0 found
        check1 = check2
        check2 += step
        if check2 >= last and last > 0 or check2 <= 0 and last == 0:
            return -1  # there is no non-transparent pixel
    if check2 - check1 <= 1:
        return check2
    # search between check1 and check2 with step size of +-1
    step = int(step / abs(step))
    check2 = check1 + step
    while True:
        pos[index] = check2
        if image.get_at(tuple(pos))[3] != 0:
            return check2  # pixel with alpha != 0 found  
        check2 += step
        

# check if there is at least one pixel where both images have non-zero
# alpha values. image1 is the avatar, image2 is the ostacle. The offset
# is defined as center(image1) - center(image2).     
def checkOverlap(image1, image2, offX, offY, step, direction):
    rect1 = image1.get_rect()
    rect2 = image2.get_rect()
    left = max(rect1.left, rect2.left - offX)
    right = min(rect1.right - 1, rect2.right - offX - 1)
    top = max(rect1.top, rect2.top - offY)
    bottom = min(rect1.bottom - 1, rect2.bottom - offY - 1)
    step2 = 2
    #print('bob: ', end='')
    #print([left, right, top, bottom, offX, offY])
    if left == right or top == bottom:
        return False, (0, 0)
    if direction == 0:  # monkey on the left
        check = bottom
        while True:
            monkeyPix = firstPixel(image1, check, step2, right - left, 1)
            obstPix = firstPixel(image2, check + offY, step2, right - left, 0)
            if monkeyPix > obstPix and monkeyPix != -1 and obstPix != -1:
                return True, (monkeyPix, check)
            check += step
            if check >= top:
                return False, (0, 0)
    elif direction == 1:  # monkey on the right
        check = bottom
        while True:
            monkeyPix = firstPixel(image1, check, step2, right - left, 0)
            obstPix = firstPixel(image2, check + offY, step2, right - left, 1)
            if monkeyPix < obstPix and monkeyPix != -1 and obstPix != -1:
                return True, (monkeyPix, check)
            check += step
            if check >= top:
                return False, (0, 0)
    elif direction == 2:  # monkey on the top
        check = left
        while True:
            monkeyPix = firstPixel(image1, check, step2, bottom - top, 3)
            obstPix = firstPixel(image2, check + offX, step2, bottom - top, 2)
            if monkeyPix > obstPix and monkeyPix != -1 and obstPix != -1:
                return True, (check, monkeyPix)
            check += step
            if check >= right:
                return False, (0, 0)
    elif direction == 3:  # monkey on the bottom
        check = left
        while True:
            monkeyPix = firstPixel(image1, check, step2, bottom - top, 2)
            obstPix = firstPixel(image2, check + offX, step2, bottom - top, 3)
            if monkeyPix < obstPix and monkeyPix != -1 and obstPix != -1:
                return True, (check, monkeyPix)
            check += step
            if check >= right:
                return False, (0, 0)


def collisionDetect(mon, obj):
    posM = [mon.xpos, mon.ypos]
    sizeM = [mon.widthRot, mon.hightRot]
    posO = [obj.xpos, obj.ypos]
    sizeO = [obj.width, obj.hight]
    # first lets check if there is an overlap in x-direction
    if posM[0] + sizeM[0] < posO[0] or posM[0] > posO[0] + sizeO[0]:
        return False
    # second we check for an overlap in y-direction
    # keep in mind that y=0 corresponds to the top of the screen!
    if posM[1] + sizeM[1] < posO[1] or posM[1] > posO[1] + sizeO[1]:
        return False
    # if there is overlap in both directions we have to take a closer look
    # this is done by checking if there are any pixels where both images
    # are non-transparent (alpha != 0)
    offX = int(posM[0] - posO[0])
    offY = int(posM[1] - posO[1])
    image1 = mon.imageData
    image2 = obj.imageData
    step1 = 2
    if posM[0] + sizeM[0]/2 > posO[0] + sizeO[0]/2:  # monkey on the right
        col, pos = checkOverlap(image1, image2, offX, offY, step1, 1)
        if col:
            print(pos, end='\r')
            pygame.draw.circle(gameDisplay, white, (int(posM[0] + pos[0]), int(posM[1] + pos[1])), 10, 1)
            return True
    else:  # monkey on the left
        col, pos = checkOverlap(image1, image2, offX, offY, step1, 0)
        if col:
            print(pos, end='\r')
            pygame.draw.circle(gameDisplay, white, (int(posM[0] + pos[0]), int(posM[1] + pos[1])), 10, 1)
            return True
    if posM[1] + sizeM[1]/2 > posO[1] + sizeO[1]/2:  # monkey on the bottom 
        col, pos = checkOverlap(image1, image2, offX, offY, step1, 3)
        if col:
            print(pos, end='\r')
            pygame.draw.circle(gameDisplay, white, (int(posM[0] + pos[0]), int(posM[1] + pos[1])), 10, 1)
            return True
    else:  # monkey on the top
        col, pos = checkOverlap(image1, image2, offX, offY, step1, 2)
        if col:
            print(pos, end='\r')
            pygame.draw.circle(gameDisplay, white, (int(posM[0] + pos[0]), int(posM[1] + pos[1])), 10, 1)
            return True
    return False
    


gameDisplay = pygame.display.set_mode((display_x, display_y))
pygame.display.set_caption('Monkey approved')
clock = pygame.time.Clock()

jumpOn = False
gameExit = False
speed = 0
distance = 0


# initialize all elements on the start screen (monkey and trees)
monkey = avatar(0)
scoreText = messageText('SCORE: ', mainFont, red, display_x * 0.98, 20, True, 1)
speedText = messageText('SPEED: ', mainFont, red, display_x * 0.02, 20, True, -1)
gameoverText = messageText('GAME OVER', bigFont, red, display_x * 0.5, display_y * 0.5)
displayElements = fillScreen([monkey, scoreText, speedText], display_x)

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN and jumpOn == False:
            if event.key == pygame.K_LEFT and speed > -1:
                speed += -1
            if event.key == pygame.K_RIGHT and speed < maxSpeed:
                speed += 1
            if event.key == pygame.K_SPACE:
                monkey.startJump(speed)
                jumpOn = True
            if event.key == pygame.K_ESCAPE:
                gameExit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pass
    
    # update the values for text display
    distance += speed * canvasElement.relativeSpeed[3]
    scoreText.value = distance / 100
    speedText.value = speed
    
    # draw the background
    floorX = distance % floorWidth
    gameDisplay.blit(floorImage, (-floorX, 0))
    if floorX > floorWidth - display_x:
        gameDisplay.blit(floorImage, (-floorX + floorWidth - 1, 0))
    
    #remove objects that moved off-screen
    displayElements = [element for element in displayElements if
        element.xpos > -element.width]
    
    # display all elements layer by layer
    displayElements.sort(key = lambda element: element.layer)
    for element in displayElements:
        element.display(-speed)
        
    # check for collisions
    obstacles = [item for item in displayElements if item.what == 3]
    collision = False
    for item in obstacles:
        collision = collision or collisionDetect(monkey, item)
    if collision:
        gameoverText.display()
        distance = 0
            
    # add new elements
    displayElements = fillScreen(displayElements, display_x)

    canvasElement.updateLargestX(-speed)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
