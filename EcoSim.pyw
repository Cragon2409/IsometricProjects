#This is EcoSim, programmed by Samuel Price, this version finalised on 31/5/21


#======================
#IMPORTING
#======================
import pygame
from random import randrange
from math import sqrt,sin,pi,cos,tan,e,atan
from GFunctions import *
from os import remove

#======================
###CONSTANTS
#======================

dw,dh = (1200,800)#defines the screen width and height
sCent = [dw/2,dh/2]#defines the screen center
sRect = [0,0,dw,dh]#defines the screen rectangle
eSRect = [-100,-100,dw+200,dh+200]#defines the extended screen rectangle
sCorners = findRectCorners(sRect)#defines the corners of the screen

NEIGHBOUR_REL_P = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]#defines the neighbouring relative positions
NEIGHBOUR_MAG_P = [magnitude(i) for i in NEIGHBOUR_REL_P]#defines the magnitude of each of the neighbouring relative positions

moveDi = {pygame.K_DOWN:[-1,1],pygame.K_UP:[1,-1],pygame.K_RIGHT:[-1,-1],pygame.K_LEFT:[1,1] }#defines the creature movement keys and the change in position
zDi =  {5:0.9 , 4:1.11}#stores the mouse button (scroll wheel) and realted numbers for zooming in and out
kDi = {pygame.K_w:[0,1] ,pygame.K_d:[-1,0], pygame.K_s:[0,-1], pygame.K_a:[1,0]}#stores the buttons for the relevant change in camera position

gridW,gridH = 80,80#defines the grid width and height
gridRect = [0,0,gridW,gridH]#defines the grid rectangle

B_DIM = [30,30]#defines the button dimensions
B_T = 25#defines the border thickness
A_B_POS = [B_T+10]*2#defines the analytics button position
TM_B_POS = dA(A_B_POS,[50,0])#defines the time multiplier button position
TM_B_MIDPOINT = dA(TM_B_POS,dD(B_DIM,[2,2]))#defines the midpoint of the time mulitplier button
E_B_POS = dA(A_B_POS,[100,0])#defines the exit button position
E_B_MIDPOINT = dA(E_B_POS,dD(B_DIM,[2,2]))#defines the exit button midpoint

P_M_RECT = [dw-B_T-210,B_T+10,200,180+30]#defines the possession menu rectangle
P_S_RECT = [P_M_RECT[0]+10, P_M_RECT[1] + P_M_RECT[3] - 50 ,30,30]#defines the possession sight toggle button
P_Q_RECT = [P_M_RECT[0]-230,P_M_RECT[1],200,90]#defines the possession quest menu rectangle
P_QS_RECT= [P_Q_RECT[0]+20,P_Q_RECT[1]+40,160,30]#defines the possession quest showing bar rectangle 
P_T_POS = [B_T+3,dh-B_T-20]#defines the possession text pos, showing the cause of death

aIcon = pygame.transform.scale(pygame.image.load("Sprites\\AnalyticsIcon.png"),B_DIM)#imports and defines the analytics icon
bCol = [130,170,210]#defines the border colour
hCol = [i*0.8 for i in bCol]#defines the secondary border colour

ANIMAL_INPUT_TYPES = [str,float,int,float,int,int,int]#defines the different animal input types for typecasting
ANIMAL_INPUT_FIELDS= ["Species","Diet","InitialPopulation","Lifespan","Hunger","Thirst","Clutch"]#defines the attribute names for animals

PLANT_INPUT_TYPES = [str,int,float,int]#defines the different plant input types for typecasting
PLANT_INPUT_FIELDS= ["Species","Abundance","Lifespan","SaplingNum"]#defines the attribute names for plants

PRESET_QUEST_TEXT = ["Eat 5 Rabbits", "Drink Water", "End All Rabbits","Survive"]#defines the quest float text

TERRAIN_TYPES = ["Plains","Desert","Snow"]#defines the different terrain type names

MATURATION_PER = 0.30#defines maturation as a ratio of lifespan
GESTATION_PER = 0.20#defines gestation duration as a ratio of lifespan
ANIMAL_SPEED_BASE = 0.12#defines the base speed of animals
NEIGHBOUR_REL = [ [c//3 - 1, c%3 - 1] for c in range(9) if c != 4 ]#defines the relative neighbour positions without (0,0).

DAY_DURATION = 2400#defines the duration of a day
AGE_T_INTERVAL = 120#defines the duration of one time interval, for age ticks
AGE_ADD = round(1/(DAY_DURATION//AGE_T_INTERVAL),4)#defines how much age is added per interval.
RANDOM_T_INTERVAL = 400#defines the random tick interval

WANDER_MAX = 60#defines how many ticks animals will wander for after being stuck

possessSprites = [pygame.transform.scale(pygame.image.load("Sprites\\"+st + "Sprite.png"),[20,20]) for st in ["Food","Water","Life","Gestation","View","Breeding","Back"]]#imports and defines the different possession bar sprites
possessSprites2= [pygame.transform.scale(pygame.image.load("Sprites\\"+st + "Sprite.png"),[30,30]) for st in ["Biting","Drinking","View","Breeding","Back"]]#imports and defines the different possession action sprites
possessChars = ['E','Q','Z','C','X']#defines the different keys used for possession actions

DEBUG = False#defines the debug variable, toggles console logs

NUM_RANGE  = list(range(ord('0'),ord('0')+10))+[ord('.')]#defines the character range of numbers, including a decimal point
CHAR_RANGE = list(range(32,127))#defines the character range of title characters

logo = pygame.image.load("Sprites\\logo.png")#imports and stores the logo image
logoDim = (500,800)#defines the dimensions of the logo
logoPos = dS([dw,dh],logoDim)#determines the drawing position of the 


THRESHOLD = 0.4#defines the terrain threshold
N3 = 2.3#defines the terrain generation power
fInfo = [(-0.12,0.63),(0.43,2.8),(1.21,5.26),(0.98,-5.2),(2.1,3.16),(0.97,2)]#defines the terrain generation paramters (part 1)
fInfo2 = [(-0.22,0.68),(0.61,2.8),(2.21,5.26),(0.48,-5.2),(3.1,3.16),(2.97,2)]#defines the terrain generation paramters (part 2)
mZoom = 4#defines the terrain generation zoom

AMP = sum([ (N3**(-(c//2))) for c in range(len(fInfo))])#determines and defines the maximum amplitude of the terrain

hLi = [-0.7,-1]#defines the height of tiles with reference to their tile idea
W_ID,L_ID = 0,1#defines the tile IDs

CHUNK_SIZE = 5#defines the size of chunks for the chunking algorithm
chunks = dict()#initialises the chunks dictionary

POPULATION_SCALE = 1#determines the scale at which to cut the population

ZOOM_MAX_LEVEL = 20#determines the amount of zoom levels
BASE_ZOOM = 20#determines the minimum zoom
ZOOM_LEVELS = [BASE_ZOOM*(1.1)**n for n in range(ZOOM_MAX_LEVEL)]#generates an arry of zoom levels

t = 51#defines the vertical camera angle
theta = 3.926#defines the horizontal camera angle
V = sin((pi/180)*t)#determines and defines sin of the vertical camera angle
C = cos((pi/180)*t)#determines and defines cos of the vertical camera angle
st1 = sin(theta)#determines and defines sin of the horizontal camera angle
ct1 = cos(theta)#determines and defines cos of the horizontal camera angle

gZ = -1#sets the global Z value as -1

pygame.init()#initialises pygame
screen = pygame.display.set_mode((dw,dh))#initialises the pygame screen with the screen width and height
clock = pygame.time.Clock()#initialises the pygame clock

pygame.font.init()#initialises the pygame font system

#imports fonts
myFont = pygame.font.SysFont("monospace", 20)
myFont2 = pygame.font.SysFont("monospace", 15)
fancyFont = pygame.font.SysFont("calibri", 22)
bigfont = pygame.font.SysFont("monospace", 50)
smallFont = pygame.font.SysFont("monospace",15)
myFontSize = myFont.render(' ', True, white).get_rect()[2]#determines and defines the width of a single monospaced character of 'myFont'

capText = "Ecosystem Simulator"#defines the caption text
pygame.display.set_caption(capText)#sets the caption text according to the constant

pygame.display.set_icon(pygame.image.load('Sprites\\FoxIcon.png'))#sets the window icon

PDU = pygame.display.update#shortens typen and code

#======================
#GRAPHICS SETUP
#======================
def simpleText(inputText,co=(0,0),colour=[255]*3,font = myFont):#draws text to the screen from with the given position on the top left of the text
    text = font.render(inputText, True, colour)#renders the text
    screen.blit(text,co)#blits the text to the screen
def centText(inputText,center,colour=white,font=myFont):#draws text to the screen anchored on the centre of the given position
    textSurf, textRect = textObjects(inputText,font,colour)#generates the text surface and rectangle
    textRect.center = center#centres the text
    screen.blit(textSurf,textRect)#blits the text to the screen
    
def rToD(co):#turns real coordinates into draw coordinates through a projection formula
    return [ zoom*(st1*co[0]+ct1*co[1]) + add[0] , zoom*C*(ct1*co[0]-st1*co[1]) + co[2]*V*zoom + add[1] ]
def dToR(co,z=0):#turns drawing coordinates into real coordinates (given z) through an inverted projection formula
    yR = st1 * ( (co[1]-add[1]-V*z*zoom) / (-zoom*C) + ct1*((co[0]-add[0])/(zoom*st1)))
    xR = (co[0]-add[0]-zoom*ct1*yR) / (zoom*st1)
    return [xR,yR]

def setView(rCo,dCo=[dw//2,dh//2]):#returns the needed camera offset to make a certain real coordinate appear at a given screen coordinate
    return [ dCo[0]-zoom*(sin(theta)*rCo[0]+cos(theta)*rCo[1]) , dCo[1]-zoom*C*(cos(theta)*rCo[0]-sin(theta)*rCo[1])-zoom*V*rCo[2] ]

def drawRectPrism(rectPrism,colour,bT=0,surface=screen):#draws a rectangular prism of [x,y,z,width,height,length] of given colour, and returns wether or not it was drawn on the screen.
    li = [rToD(co+[rectPrism[2]]) for co in findRectCorners(rectPrism[:2] + rectPrism[3:5])]#determines and defines the first horizontal polygon
    li2 = [rToD(co+[rectPrism[2]+rectPrism[5]]) for co in findRectCorners(rectPrism[:2] + rectPrism[3:5])]#determines and defines the second horizontal polygon
    for n in range(2,4): pygame.draw.polygon(surface,[i1*0.9 for i1 in colour] ,[li[n],li2[n],li2[(n+1)%4],li[(n+1)%4]])#draws the polygons between the two horizontal polygons
    pygame.draw.polygon(surface,colour,li)#draws the first (top) horizontal polygon)

def transpPolygon(colour,points,opacity=200,blSurface=screen):#draws a polygon with a given transparency
    tL,bR = minCorner(points,2),maxCorner(points,2)#determines the top left and bottom right points of the polygon
    points = [dS(i,tL) for i in points]#reframes the points to the top left
    surface = pygame.Surface((dS(bR,tL)), pygame.SRCALPHA, 32)#creates a temporary surface with the dimensions of the polygon
    pygame.draw.polygon(surface,list(colour)+[opacity],points)#draws the polygon to the temporary surface
    screen.blit(blSurface,tL)#draws the temporary surface to the given surface
    
def drawTranspRectPrism(rectPrism,colour,bT=0,surface=screen,opacity=200):#draws a rectangular prism of [x,y,z,width,height,length] of given colour
    li = [rToD(co+[rectPrism[2]]) for co in findRectCorners(rectPrism[:2] + rectPrism[3:5])]
    transpPolygon(colour,li,opacity,surface)
    pygame.draw.polygon(surface,colour+[opacity],li)

def drawRectPoly(re,colour,bT=0):#draws a rectangular prism rotated in any direction
    pos,a,b,c = tuple(re)
    li = [rToD(nAdd(pos,i)) for i in [ [0,0,0] , a , nAdd(a,b) , b ]]
    li2 = [rToD(nAdd(pos,nAdd(i,c))) for i in [ [0,0,0] , a , nAdd(a,b) , b ]]
    for n in range(0,4): pygame.draw.polygon(screen,[i1*0.9 for i1 in colour] ,[li[n],li2[n],li2[(n+1)%4],li[(n+1)%4]])
    pygame.draw.polygon(screen,colour,li)

def drawPSim(pos):#draws a blue dot, given the position of the possessed animal
    z = gZ - 2#determines the vertical position of the dot
    pygame.draw.circle(screen,blue,dF(rToD(pos+[z])),5)
#======================
###FUNCTIONS SETUP
#======================
#chunks are stored as strings '2_1', with the numbers being the floor division of the position by the chunk size, seperated by an underscore and stored as a string
def rPTC(rPos): return pTC([int(i//CHUNK_SIZE) for i in rPos])#converts real position into the converted chunk position
def pTC(pos): return '_'.join([str(i) for i in pos])#converts the number chunk position into the string chunk position
def cTP(chunk): return [int(i) for i in chunk.split('_')]#convers the string chunk position into the number chunk position
def nChunks(chunk):#returns the neighbouring chunks from a given string chunk position
    cPos = cTP(chunk)#defines the number chunk position
    return [pTC(dA(cPos,r)) for r in NEIGHBOUR_REL]#returns the string chunk position of each neighbouring chunk

def chunkAdd(item,chunk):#adds an item to a given chunk
    if chunk in chunks: chunks[chunk].append(item)
    else: chunks[chunk] = [item]
def chunkRemove(item,chunk):#removes an item from a given chunk, assuming it is already there
    chunks[chunk].remove(item)
    if chunks[chunk] == []: del chunks[chunk]
def chunkSearch(chunk):#returns all contents of a chunk if it exists, and an empty list otherwise
    if chunk in chunks: return chunks[chunk][:]
    else: return []
def chunkColSearch(chunk,exclude):#returns the entities in and around a given chunk, excluding the given entity.
    entities = chunkSearch(chunk)[:]
    entities.remove(exclude)
    for chunk in nChunks(chunk): entities += chunkSearch(chunk)
    return entities
def chunkExactCheck(position,fil=lambda x : True if x.eType == "Plant" else False):#Returns true if an entity is on that tile using the chunking system, returns false if otherwise
    position = dF(position)
    chunk = rPTC(position)
    for entity in chunkSearch(chunk):
        if dF(entity.pos) == position and fil(entity): return True
    return False

def terrainGenerationFunction(x,y,xA=0,yA=0):#using the terrain generation formula with an x, a y, and offsets for both, returning a number.
    x += xA; y += yA
    x /= mZoom; y /= mZoom
    return sum([ (N3**(-(c//2)))*(cos(i[0]*x+i[1])*sin(fInfo2[c][0]*y+fInfo2[c][1])) for c,i in enumerate(fInfo) ])
def terrainNumberConvert(x): return (x+AMP)/(2*AMP)#takes the output of the terrain generation formula, and represents it in between 0 and 1.

def tileData(n,tType=0):#returns the tile ID and colour of a given tile, given the formula output and the terrain type
    n = terrainNumberConvert(n)
    if n < THRESHOLD:
        n *= 0.8
        t = W_ID
        col = [0,255*n,255*(1-n)]
    else:
        cN2 = (n-THRESHOLD)/(1-THRESHOLD)
        cN3 = 1 - cN2
        t = L_ID
        if tType == 0: col = [40,210*(1-cN2),cN2]#plains
        elif tType == 1: col = [255,100+127*cN2,0]#desert
        elif tType == 2: col = [80 + 120*cN2, 160 + 95*cN2, 176 + 79*cN2]#snow
    return t,col

def showTablePers(surface=screen):#generates the table onto a given surface
    xNeg,bDi = 0,1
    bMax = gridH
    b = -gridW
    x_rMin = 0
    x_rMax = gridW
    while b < bMax+3:
        x = x_rMin
        while x != x_rMax:
            y = x + b
            if inRect((x,y),[0,0,gridW,gridH]):#checks if the tile is inside of the grid
                tType,col = table[y][x],tableCol[y][x]#obtains the tile ID
                h = hLi[tType]
                if tType == W_ID: drawTranspRectPrism([x,y,h]+[1,1,-h],col,b,surface=surface,opacity=200)
                else: drawRectPrism([x,y,h]+[1,1,-h],col,b,surface=surface)#draws the rectangular prism with matching data to the tile
            x += 1
        b += bDi

def testValidFloat(st): return len(st) > 0 and st.count('.') <= 1 and st[0] != '.'#tests whether a string is a valid float, given that it is only made of integers and decimal point(s)

def gradientList(startColour,endColour,iterations=200):#generates a gradient list given a start, end, and amount of iterations
    out = []
    avColour = ((endColour[0]-startColour[0])/iterations,(endColour[1]-startColour[1])/iterations,(endColour[2]-startColour[2])/iterations)
    for n in range(iterations): out.append(((avColour[0]*n+startColour[0]),(avColour[1]*n+startColour[1]),(avColour[2]*n+startColour[2])))
    return out
def mixedRect(colourList,startX,startY,width,height):#draws a rectangle with a gradient, given the rectangle and the gradient list
    step = (height/len(colourList))//1
    for c,n in enumerate(colourList): pygame.draw.rect(screen,n,(startX,startY+c*step,width,step))
def listReplace(li,ele,rep):#replaces elements in lists given the list, the element, and the replacement
    out = []
    for i in li:
        if i == ele: out.append(rep)
        else: out.append(i)
    return out
class GradBackground:#the gradient background class, used for the day night cycle
    def __init__(self,colour1,colour2):
        self.colour1,self.colour2 = colour1,colour2#stores the two colours, where the none items are placed with the gradient element
        self.ticks = 0#stores the current time/progress of the gradient
        
        self.starLi = [ ([randrange(100,256) for n in range(3)],[randrange(0,dw),randrange(0,dh)]) for n in range(150)]#generates a list of 150 star positions for the background
        self.starSurface = pygame.Surface([dw,dh],pygame.SRCALPHA,32)#initialises a surface for the stars to be drawn on
        self.starSurface.fill([0,0,0,0])#makes that surface entirely transparent
        
    def update(self,ticks):
        ticks /= 4.71#convers the ticks into the day night cycle duration
        if ticks%511 > 255: colourN = 255-(ticks%511-255)#puts the gradient to second phase
        else: colourN = ticks%511
        
        sTicks = ticks - 100#generates the star ticks, which are out of phase with the background ticks
        if sTicks%511 > 255: alpha = max(0,int(2*(128 - abs( (sTicks%511 - 256) - 128 ) )))#if stars are being shown, calculates and stores the alpha value, reaching its' peak in the middle and falling to zero on either side
        else: alpha = 0#sets the alpha to zero if stars should not be shown
            
        tempList = gradientList(listReplace(self.colour1,None,colourN),listReplace(self.colour2,None,colourN),dh)#generates the gradient list, using the stored colours, ticks, and the gradient elements
        mixedRect(tempList,0,0,dw,dh)#draws the background over the whole screen
        
        if alpha != 0:#if the alpha is not zero
            for col,i in self.starLi: pygame.draw.circle(self.starSurface,col + [alpha], i, 2)#redraws the stars with appropiate alpha values
            screen.blit(self.starSurface,(0,0))#draws the star surface onto the screen

def pGKey(item):#returns the water distance of a given tile, either as a water tile +relative position distance or a tile that already has water distance information + relative position distance
    c,i = item
    add = NEIGHBOUR_MAG_P[c]
    if table[i[1]][i[0]] == W_ID: return 0 + add
    else: return i[1] + add

def arrayCopy(iLi): return [i.copy()[:] for i in iLi[:]]
def genPath():#generates a table that holds the optimum distance and direction to go to water
    tableWP = [[None for x in range(gridW)] for y in range(gridH)]# stores information for any tile as [ (direction X, direction Y), distance ]
    emptyTile = True#initialise the loop exit condition
    while emptyTile:#initialise the while loop with the emptyTile condition, as once no tiles are filled in during a loop, the process is complete
        bTableWP = arrayCopy(tableWP)#copies the aray as a value, rather than reference, to a buffer table so it doesnt call on itself
        emptyTile = False#resets the loop exit condition
        for y,row in enumerate(tableWP):#loops through the y coordinate and the row of the table
            for x,i in enumerate(row):#loops through the x coordinate and the item of the row
                if i == None and table[y][x] == L_ID:#checks that there isn't information yet and that the position is on land
                    emptyTile = True#resets the loop exit condition
                    ns = [dA(i,(x,y)) for i in NEIGHBOUR_REL_P]
                    ns = [(c,i) for c,i in enumerate(ns) if inRect(i,gridRect) and (tableWP[i[1]][i[0]] != None or table[i[1]][i[0]] == W_ID)]
                    if ns != []:
                        mItem = min(ns,key=pGKey)[1]
                        di = dS(mItem,[x,y])
                        dist = magnitude(di)
                        if table[mItem[1]][mItem[0]] == W_ID:
                            bTableWP[y][x] = [di,dist]
                            
                        else:
                            bTableWP[y][x] = [di,dist+tableWP[mItem[1]][mItem[0]][1]]
        tableWP = arrayCopy(bTableWP)#copies over the next table
    return tableWP#returns the water pathfinding table

def getItem(pos): return table[pos[1]][pos[0]]#returns the item at a given position in the table

def randomPos(): return [randrange(0,gridW),randrange(0,gridH)]#generates a random position on the table

def choosePos(pPos=None):#decideds a position for a new entity, either given a parent position to be around or any random position.
    if pPos == None:#chesk if there is no parent position
        pos = randomPos()#generates a random position
        while getItem(pos) == W_ID:#checks if the table is water at that position
            pos = randomPos()#generates a random position
    else:
        pos = [pPos[n]+randrange(-2,3) for n in range(2)]#generates a position nearby the parent position
        counter = 0#initialises the counter
        while (pos == pPos or (not inRect(pos,[0,0,gridW,gridH])) or getItem(pos) == W_ID or (chunkExactCheck(pos))) and counter < 20:#checks the position is not collideing with another entity, in water, or that the counter has gone too high
            pos = [pPos[n]+randrange(-2,3) for n in range(2)]
            counter += 1
        if counter == 20: pos = None#gives up if it trys too many times
    return pos#returns the chosen position

#======================
#Entity Setup
#======================



def foodEval(age,m=1): return m*0.82*( ((4.5*age-2.7)**2 + 1) / ((4.5*age-2.7)**4 + 1))#evaluates the utility of food given the age/lifespan of the food
def speedEval(age,m=1): return m*max(ANIMAL_SPEED_BASE*(-3.5*(age - 0.5)**2 + 1),0.125*ANIMAL_SPEED_BASE)#evaluates the speeed of an animal given the speed base and age/lifespan

#For Diet, 0 - Herbivore | 1 - Carnivore | 0 < x < 1 - Omnivore, representing percentage
class Animal:#The animal class, for all in-simulation animals, given by a dictionary reference with all attributes given.
    eType = "Animal"#sets the entity type as animal
    def __init__(self,dictRef,pPos=None):#initialises an animal, given the dictionary reference and a parent position
        self.dictRef = dictRef#stores the dictonary reference for reproduction
        self.name,self.diet,initialPopulation, self.lifespan, self.hungerD,self.thirstD,self.clutch = tuple([dictRef[i] for i in ANIMAL_INPUT_FIELDS])#stores the animal attributes

        self.chooseSpawn(pPos)#decides the spawn
        self.maturation = self.lifespan*MATURATION_PER#calculates and defines the time of maturation
        self.gestation = self.lifespan*GESTATION_PER#calculates and defines the time of gestation
        self.gestating = False#initialises gestation flag variable
        self.gestationCounter = 0#initialises gestation counter variable to 0
        self.impregCounter = 0#initilalises impregnation counter variable to 0
        self.alive = True#initialises alive flag variable
        if pPos == None: self.age = self.lifespan*randrange(0,1000)/1000#generates a random age for the initially spawned animals that don't have parents
        else: self.age = 0#initialises age variable to 0
        
        #initialises hunger, thirst, and their respective gradients over time
        self.hunger = 1
        self.thirst = 1
        self.hungerG = self.hungerD/AGE_T_INTERVAL
        self.thirstG = self.thirstD/AGE_T_INTERVAL

        self.target = self.targetT = None#initialises the target entity and tile variables for the AI

        self.rotation = randrange(0,250)/1000#assigns a randomised rotation

        self.possessed = False#initialises possessed boolean variable
        self.possessedView = 0#Initialises view setting,  0 - Free Cam | 1 - Lock Centre
        self.dMode = False#debug mode initialisation, prints priority when enabled
        self.wanderPhase = 0#initialises the wander phase counter

        self.questStorage = self.eAte = self.waterDrank = 0#for presets only, stores quest progress as well as eating and drink statistics
        self.pShowLen = 5#stores the possession action show length
    def chooseSpawn(self,pPos=None):#generates the spawnpoint and initialises it's chunk position if it successfully finds a position
        self.pos = choosePos(pPos)
        if self.pos != None:
            self.chunk = rPTC(self.pos)
            chunkAdd(self,self.chunk)
            self.bStore = self.pos[1]-self.pos[0]
    def chunkUpdate(self):#updates the chunk position
        nC = rPTC(self.pos)#determines new chunk
        if nC != self.chunk:#checks if chunk has changed
            chunkRemove(self,self.chunk)#removing self from old chunk
            chunkAdd(self,nC)#adding self to new chunk
            self.chunk = nC#assining new chunk
    def draw(self):#draws the model, baby if not matured, adult otherwise
        if self.age >= self.maturation: models[self.name].draw(self.pos+[gZ],self.rotation)
        else: models[self.name+"Baby"].draw(self.pos+[gZ],self.rotation)
        if self.possessed: drawPSim(self.pos[:2])#if possessed, draws the simulation dot possession symbol
    def randomTick(self):#random ticks function, for randomised events, not currently used for animals
        pass
    def update(self):#simulates and updates the animals within the simulation
        if self.alive:
            if self.thirst <= 0:#thirst check
                self.die("thirst")#kills by thirst
            elif self.hunger <= 0:#starvation check
                self.die("hunger")#kills by hunger
            elif not self.possessed:#priority system
                if self.wanderPhase > 0:#tests if wanderphase is active
                    self.wanderPhase -= 1#decremements the wanderphase counter
                    priority = "wander"#overrides the priority as wandering during the wanderphase
                elif self.age > self.maturation and self.gestationCounter == 0 and self.hunger > 0.7 and self.thirst > 0.7 and (not self.gestating) and self.impregCounter == 0:#checks if eligable for mating
                    priority = "mating"
                elif self.hunger < 0.7 or self.thirst < 0.7:#checks if gathering/hunting is required
                    priority = min([ (self.hunger,"food") , (self.thirst,"water") ],key=lambda x : x[0])[1]#decides the priority by whichever stat is lower
                else:
                    priority = "wander"#if nothing else, makes the animal wander around until it finds something

                if priority == "food":#food hunting actions
                    entities = chunkColSearch(self.chunk,self)#lists all entities in the neighbour chunk except itself
                    if self.diet == 0:#herbivore
                        entities = [i for i in entities if i.eType == "Plant"]#sets list to only plants for herbivores
                    elif self.diet == 1:#carnivore
                        entities = [i for i in entities if i.eType == "Animal" and i.name != self.name]#sets list to only animals that aren't itself for carnivores
                    if entities == []:#wandering
                        priority = "wander"#makes the animal wander if it can't do anything else
                    else:#eating process
                        target = min(entities,key=lambda x: coDistance(self.pos,x.pos))#finds the closest target
                        self.targetT = None#resets the class bound target tile variable
                        targetT = dA(dF(target.pos),[0.5]*2)#sets the function scope variable to be equal to the middle of the tile the entity is on
                        dist = coDistance(self.pos,targetT)#determines distance to the target square
                        sPos = dA(dF(self.pos),[0.5]*2)#determines middle of own tile
                        posList = [dA(sPos,i) for i in NEIGHBOUR_REL]#generates array of positions around self
                        mList = [i for i in posList if inRect(i,gridRect) and table[int(i[1])][int(i[0])] == L_ID]#generates array of possible movement positions around self
                        if mList == []: priority = "wander"#in case of no valid tiles, wander instead
                        else:#if there are valid tiles
                            mItem = min(mList,key = lambda x: coDistance(x,targetT))#find the tile least distant from the target
                            if dist < 1: self.eat(target)#if distance < 1, eat the target
                            elif not self.move(dS(mItem,self.pos)):#attempts to move the player, and if unsuccessful(hit a wall/riverbank)
                                    #unsuccessful movement
                                    self.wanderPhase = WANDER_MAX#begin a wanderphase
                                    priority = "wander"#set priority to wander
                    
                elif priority == "water":#drinking process
                    self.targetT = None#resets the class bound target tile variable
                    sCo = dF(self.pos)#generates the tile the animal is on
                    di,dist = tableWP[sCo[1]][sCo[0]]#obtains the direction and distance from the water pathfinding table
                    if dist <= 1.5: self.drink()#if the water is only tile away (straight or diagonal), drink
                    else: self.move(di)#otherwise, move towards the water
                    
                elif priority == "mating":#mating process
                    entities = chunkColSearch(self.chunk,self)#generates an array of all entities in neighbouring chunks
                    entities = [i for i in entities if i.eType == "Animal" and i.name == self.name and i.age >= i.maturation and i.impregCounter == 0 and i.gestationCounter == 0]#filters list by eligable mates
                    if entities != []:#if there are eligable mates in range
                        self.targetT = None#reset the class bound target tile variable
                        target = min(entities,key=lambda x: coDistance(self.pos,x.pos))#determines closest mate
                        dist = coDistance(target.pos,self.pos)#generates and defines distance of closest mate
                        if dist < 1:#if they are in range
                            target.gestating = True#sets the mate to pregnant
                            target.gestationCounter = target.gestation#sets the mates gestation counter
                            self.impregCounter = self.gestation#sets own cooldown for impregnation
                        else:#if they are not in range
                            self.move(dS(target.pos,self.pos))#moves towards mate
                    else: priority = "wander"#sets the priority to wander if there are no eligable mates nearby
                if self.dMode:print(priority)#for class based debug mode, prints the priority
                    
                if priority == "wander":#wandering process
                    if self.targetT == None or coDistance(self.pos,self.targetT) < 2:#if there is no class bound target tile set or it's less than two tiles away
                        self.targetT = [self.pos[n]+randrange(-CHUNK_SIZE*2,CHUNK_SIZE*2+1) for n in range(2)]#decides the class bound target tile
                        while coDistance(self.pos,self.targetT) < 2 or (not inRect(self.targetT,gridRect)) or table[int(self.targetT[1])][int(self.targetT[0])] == W_ID:#checks if the class bound target tile is eligable
                            self.targetT = [self.pos[n]+randrange(-CHUNK_SIZE*2,CHUNK_SIZE*2+1) for n in range(2)]#decides the class bound target tile
                    if not self.move(dS(self.targetT,self.pos)):#moves towards the class bound target tile, but if it fails to move
                        self.targetT = [self.pos[n]+randrange(-CHUNK_SIZE*2,CHUNK_SIZE*2+1) for n in range(2)]#decides the class bound target tile
                        while coDistance(self.pos,self.targetT) < 2 or (not inRect(self.targetT,gridRect)) or table[int(self.targetT[1])][int(self.targetT[0])] == W_ID:#checks if the class bound target tile is eligable
                            self.targetT = [self.pos[n]+randrange(-CHUNK_SIZE*2,CHUNK_SIZE*2+1) for n in range(2)]#decides the class bound target tile
        
        return self.alive#returns alive flag
    def ageAdd(self,add=1):#conducts age related processes on the animal
        if self.alive:#only runs if it's alive
            if self.gestating:#if the animal is gestating
                self.gestationCounter -= add#decrement the gestation counter
                if self.gestationCounter <= 0:#if the gestation is over
                    self.reproduce()#reproduce
                    self.gestationCounter = -self.gestation#set gestation cooldown
                    self.gestating = False#disable the gestation flag 
            elif self.gestationCounter < 0:#if the gestation cooldown is active
                self.gestationCounter += add#increment the gestation cooldown
                if self.gestationCounter > 0:#if the gestation counter is above 0
                    self.gestationCounter = 0#set the gestation counter to exactly 0
            elif self.impregCounter > 0:#if the impregnation cooldown is active
                self.impregCounter -= add#decrement the impregnation cooldown
                if self.impregCounter < 0:#if the impregnation counter is less than 0
                    self.impregCounter = 0#set the impregnation counter to exactly 0

        self.age += add#increment age
        if self.age > self.lifespan: self.die("old age")#if age is greater than lifespan, die by old age
        
        self.hunger -= self.hungerG#decrement hunger variable
        self.thirst -= self.thirstG#decrement thirst variable
        
    def die(self,cause=''):#kills the animal, and records a cause of death
        self.alive = False#sets the alive flag to false
        self.cause = cause#stores the cause of death
        if DEBUG: print(self.name,"died of",cause,"\nthirst",round(self.thirst,2),"hunger",round(self.hunger,2),"Age",round(self.age/self.lifespan,2),'\n')#on debug mode, prints cause of death and stats
        chunkRemove(self,self.chunk)#removes self from the current chunk
    def drink(self):#drinks water
        self.thirst = 1#resets thirst to 1
        self.waterDrank += 1#increments waterDrank statistic variable
    def eat(self,entity):#eats and kills 
        regain = foodEval(entity.age/entity.lifespan)#change this
        self.eAte += 1#increments entities ate statistics variable

        #implementation of saturation hunger system, diminishing returns for eating more and more
        if self.hunger > 1:
            satScore = satICalc(self.hunger-1)
            self.hunger = 1 + satCalc(satScore+regain)
        else:
            cLost = 1 - self.hunger
            if regain > cLost:
                saturation = satCalc(regain - cLost)
                self.hunger = 1 + saturation
            else:
                self.hunger += regain
                
        if entity.alive: entity.die("Predation")#kills the eaten entity
    def move(self,di):#take direction, return 1 if successful, 0 if not
        self.rotation = twoCoAngle((0,0),di)#sets the rotation to face direction of movement
        if self.alive:#if currently alive
            speed = speedEval(self.age/self.lifespan)#calculate and define current speed
            cha = dM(unitVec(di),[speed]*2)#calculate and define actual vector displacement
            nPos = dA(self.pos,cha)#calculate the new position
            if inRect(nPos,gridRect) and table[int(nPos[1])][int(nPos[0])] != 0:#check position validity (in grid and on land)
                self.pos = nPos#assign new position
                self.chunkUpdate()#update the chunk position
                self.bStore = self.pos[1]-self.pos[0]#store b value (view ordering algorithm)
                return  1#return 1 for successful movement
            else: return 0#return 0 for unsuccessful movement
    def reproduce(self):#produces offspring
        clutchSize = randrange(1,self.clutch+1)#determines randomised size of clutch
        for n in range(clutchSize):#for all animals in clutch
            temp = Animal(self.dictRef,[int(i) for i in self.pos])#attempts to generate a new animal
            if temp.pos != None: animals.append(temp)#if a spawn position is found, add the new animal to the animals list
    def possessionMenu(self):#run the possession menu that shows whilst possessing an animal
        keys = pygame.key.get_pressed()#get currently pressed keys
        pygame.draw.rect(screen,bCol,P_M_RECT)#draws the possession menu rectangle
        pygame.draw.rect(screen,black,P_M_RECT,2)#draws the possession menu rectangle border
        simpleText(self.name,dA(P_M_RECT[:2],(10,5)))#draws the animal/species name

        stats = [min(self.hunger,1),self.thirst,self.age/self.lifespan,abs(self.gestationCounter/self.gestation)]#generates a list of shown statistics from 0-1 for the menu bars
        if stats[3] != 0: stats[3] = 1 - stats[3]#inverts the 4th statistic
        
        x = P_M_RECT[0] + 10#calculates and defines the x coordinate for showing the statistics
        for c,i in enumerate(stats):#loops through the different statistics by their index and item
            y = P_M_RECT[1] + 30 + 10 + c*30#calculates and defines the y statistic for this statistic
            if c == 3 and self.gestationCounter < 0: col = red#makes the gestation cooldown show red if it's negative
            else: col = green#and green otherwise
            pygame.draw.rect(screen,black,[x,y,150,20])#draws a black background for the bar
            pygame.draw.rect(screen,col,[x,y,150*i,20])#draws the progress bar by the appropiate width for the statistic
            if c == 0 and self.hunger > 1: pygame.draw.rect(screen,yellow,[x,y,300*(self.hunger - 1),20])#draws saturated hunger as yellow over normal hunger
            pygame.draw.rect(screen,white,[x,y,150,20],2)#draw a border around the progress bar
            
            screen.blit(possessSprites[c],[x+160,y])#draw the sprite of the same index next to the bar

        #seperate the possession 
        P_S_POS = P_S_RECT[:2]#stores the possession seeing button position
        P_S_DIM = P_S_RECT[2:]#stores the possession seeing button dimensions
        for n in range(self.pShowLen):#loops through the first (self.pShowLen) times, 5 in normal and 4 in a preset where you can't exit possession.
            pos = dA(P_S_POS,[n*37,0])#calculates and stores the next button positon
            screen.blit(possessSprites2[n],pos)#draws the possession action sprite
            col = blue if keys[ord(possessChars[n].lower())] else black#decides the border colour, blue if key is being pressed and black otherwise
            pygame.draw.rect(screen,col,pos+P_S_DIM,2)#draws the border
            centText(possessChars[n],dA(pos,[15,40]))#draws the related action key below the sprite
    def possessEat(self):#eating action while possessed
        entities = chunkColSearch(self.chunk,self)#gets the nearby entities
        if self.diet == 0:#herbivore
            entities = [i for i in entities if i.eType == "Plant"]#makes the list only plants for herbivores
        elif self.diet == 1:#carnivore
            entities = [i for i in entities if i.eType == "Animal" and i.name != self.name]#makes list only animals of different species for carnivores
        if entities != []:#if it's not an empty list
            target = min([i for i in entities],key=lambda x : coDistance(x.pos,self.pos))#determines closest target
            if coDistance(target.pos,self.pos) < 1:#if the closest target is less than one tile away
                self.eat(target)#eats the target
                return 1#returns 1 for successful eating
    def possessDrink(self):#drinking action while possessed
        aPos = dF(self.pos)#calculates and stores own exact position
        for ne in NEIGHBOUR_REL:#goes through neighbouring position
            nPos = dA(aPos,ne)#calculates and stores neighbour position
            if inRect(nPos,gridRect):#checks if neighbouring position is inside the rectangle
                if table[nPos[1]][nPos[0]] == W_ID:#checks if the neighbouring item is in the water
                    self.drink()#drinks/restores thirst
                    return 1#returns 1 for successful drinking
    def toggleView(self):#toggle view setting for view centering
        self.possessedView = 1 - self.possessedView
    def possessBreed(self):#runs breeding while possessed
        pass#unimplemented
    def giveReadout(self):#gives the readout, a debug setting
        print('='*10)
        print(self.name,str(round(self.age,3))+" days old",sep=', ')
    def questMenu(self):#runs the quest menu
        self.questUpdate()#updates quest progress
        
        pygame.draw.rect(screen,bCol,P_Q_RECT)#draws the possession quest menu
        pygame.draw.rect(screen,black,P_Q_RECT,2)#draws the possession quest menu border
        questText = PRESET_QUEST_TEXT[self.quest]#determmines the quest text
        simpleText(questText,dA(P_Q_RECT[:2],[10,5]))#draws the quest text
        nRect = P_QS_RECT[:]#stores the progress bar width
        nRect[2] *= self.objective#changes the progress bar width for objective completion
        pygame.draw.rect(screen,green,nRect)#draws the progress bar in green
        pygame.draw.rect(screen,black,P_QS_RECT,2)
        
    def questUpdate(self):#updates quests, objective stores progress from 0 - 1, quest stores quest number, and questStorage is just an extra variable
        if self.quest == 0:#Quest 0 - Eat Rabbits
            self.objective = self.eAte/5#sets the objective to entities ate / 5.
            self.questStorage = self.waterDrank#sets the quest storage to the water drank, so after quest is completed they have to drink 1 more than they already have
        elif self.quest == 1:#Quest 1 - Drink Water
            self.objective = self.waterDrank-self.questStorage#sets the objective to drinking once more than previously
        elif self.quest == 2:#Quest 2 - Eliminate all Rabbits
            self.objective = 1 - (self.aMenu.eStats["Rabbit"][-1][1] / 500)#sets the objective to inverse of the population of rabbits, assuming the max at out at 500 from precalculated data
        else:#Quest 3 - survive
            self.objective = 1 - (self.age/self.lifespan)#sets the objective to inverse age, meaning that you could only complete it if you had 0 age.
        if self.objective >= 1: self.quest += 1#if objective is completed (>=1), go to next quest
            
        self.objective = limit(self.objective,1,0)#limit the objective between 1 and 0 for drawing reasons
        
        
    
        
class Plant:#Plants class, all plants are stored as this object, given by a dictionary referance containing all attributes
    eType= "Plant"#sets the entity type as plant
    def __init__(self,dictRef,pPos=None):#initialises a plant object, using the reference and a parent position
        self.dictRef = dictRef#stores the dictionary reference for reproduction
        self.name, abundance, self.lifespan, self.saplingNum = tuple([dictRef[i] for i in PLANT_INPUT_FIELDS])#stores the plant attributes
        self.chooseSpawn(pPos)#decides the starting position for the plant
        if pPos == None: self.age = self.lifespan*randrange(0,1000)/1000#decides a random age for initial plants, as they have no parents
        else: self.age = 0#initialises age
        self.maturation = self.lifespan*MATURATION_PER#calculates and defines the time of maturation
        self.gestation = self.lifespan*GESTATION_PER#calculates and defines the time of gestation
        self.gestationCounter = None#initialises the gestation counter to 0
        self.aQ = 0#stores the initial age quotient of 0
        self.alive = True#initialises the alive flag variable
        
        self.rotation = randrange(0,1000)/1000#picks a random rotation for the plant
    def chooseSpawn(self,pPos):#decides the spawn given a parent position, and initialises chunk position
        self.pos = choosePos(pPos)#decides spawnpoint
        if self.pos != None:#if no available position was found, initialise the chunk position
            self.chunk = rPTC(self.pos)#initialise the chunk position
            chunkAdd(self,self.chunk)#add self to chunk
            self.bStore = self.pos[1]-self.pos[0]#stores b (for view ordering)
    def draw(self):#draws self model in position, smaller if baby, normal size if adult
        if self.age >= self.maturation:#tests if maturated
            models[self.name].draw(self.pos+[gZ],self.rotation)#draws adult model in position at rotation
        else:#if not matured
            models[self.name+"Baby"].draw(self.pos+[gZ],self.rotation)#draws baby model in position at rotation
    def randomTick(self):#randomness based event runner
        if randrange(0,1000) < self.aQ: self.die()#dies at a chance based on age
    def update(self):#runs plant based updates, which is nothing
        return self.alive#returns alive flag
    def ageAdd(self,add=1):#runs aging based events on the plant
        self.age += add#increments age
        self.aQ = aQCalc(self.age,self.lifespan)#calculate age quotient for age related death
        if self.age >= self.maturation:#if matured, runs gestation events
            if self.gestationCounter != None:#tests if already gestating
                if self.gestationCounter > 0:#if the gestati
                    self.gestationCounter -= add*2
                else:#if gestationCounter has finished
                    self.reproduce()#reproduce
                    self.gestationCounter = None#rest the gestationCounter
            elif randrange(0,30) == 0:#if not already gestating, at a 1/30 chance
                self.gestationCounter = self.gestation#sets the gestation counter to the class bound gestation duration variable
    def die(self,cause=''):#kills the plant
        self.alive = False#set the alive flag to false
        chunkRemove(self,self.chunk)#removes self from chunk
    def rateFood(self):#rates food for herbivorous animals
        return 0.8#a pre-decided value for balancing
    def reproduce(self):#reproduces the plant
        cSize = randrange(0,self.saplingNum+1)#decides on an amount of saplings
        for n in range(cSize):#making (cSize) saplings
            temp = Plant(self.dictRef,[int(i) for i in self.pos])#generates and temporarily stores a plant
            if temp.pos != None:#if there it found a position to generate
                plants.append(temp)#append the new plant to the plants list
                
    def giveReadout(self):#debug function, gives information about self
        print('='*10)
        print(self.name,str(round(self.age,3))+" days old",sep=', ')
        
    


#======================
###BORDER SETUP
#======================
bSurface = pygame.Surface([dw,dh],pygame.SRCALPHA,32)#initialises the border surface with an alpha layer
def makeBorder(bT=B_T):#generates the border sprite
    bRect = [bT,bT,dw-bT*2,dh-bT*2]#calculates and stores the border outline rectangle
    bSurface.fill([0]*4)#fills the border with treansparent pixels 
    pygame.draw.rect(bSurface,[i*0.9 for i in bCol],[0,0,dw,dh],bT*2)#fills an outline around the edge of the border surface

    tileSprite = pygame.Surface([bT]*2,pygame.SRCALPHA,32)#initialises the single tile sprite
    tileSprite.fill([0]*4)#fills the tile sprite with transparent pixels
    rect = [0,0,bT,bT]#stores the rectangle for the tile sprite
    corners = findRectCorners(rect)#generates the array of coordinates that stores the corners of this rectangle
    midPoints = [dD(dA(corners[c],corners[(c+1)%4]),[2,2]) for c in range(4)]#generates the midpoints of each pair of adjacent corners
    cent = [bT/2]*2#calculates and stores the centre of each idndividual tile
    for c in range(4):#runs the loop 4 times for each of t he 4 sides of the tile
        pygame.draw.line(tileSprite,hCol,midPoints[c],midPoints[(c+1)%4],2)#draws a line from one midpoint to the next
        pygame.draw.line(tileSprite,hCol,corners[c],cent,2)#draws a line from one corner to the tile centre
    pygame.draw.polygon(tileSprite,[120,80,90,60],midPoints,2)#draws a diamond from all the midpoints
    pygame.draw.rect(tileSprite,hCol,[0,0,bT,bT],2)#draws a border arouind the tile
    IND = 5#defines the indent size of the pattern
    nRect = [IND]*2 + [bT-IND*2]*2#calculates and stores the indented rectangle
    pygame.draw.rect(tileSprite,bCol,nRect)#draws the indented rectangle to the tile sprite
    for c in range(2): pygame.draw.line(tileSprite,hCol,midPoints[c],midPoints[c+2],2)#draws a horizontal and vertical line in the tile sprite

    pygame.draw.rect(tileSprite,hCol,nRect,2)#draws a border around the indented rectangle
                        
    tileCos = [[x,0] for x in range(0,dw,bT)] + [[x,dh-bT] for x in range(0,dw,bT)] + [[0,y] for y in range(bT,dh-bT,bT)] + [[dw-bT,y] for y in range(bT,dh-bT,bT)]#determines and stores each location the tile sprite must be drawn at
    for co in tileCos: bSurface.blit(tileSprite,co)#blits the tilesprite at each position in the tileCos array

    pygame.draw.rect(bSurface,black,bRect,4)#draws a border on the interior of the border
    pygame.draw.rect(bSurface,black,[0,0,dw,dh],3)#draws a border on the exterior of the border
            
makeBorder()#generates the border sprite




#======================
###MODEL SETUP
#======================
def dataAnalyse(data):#for a given one dimensional array of data, returns the minimum, maximum, and range
    mi,ma = min(data),max(data)
    return mi,ma,ma-mi


def plotSeveral(dataList,rect,legend):#plots several arrays of [(x1,y1) , (x2,y2) ... ], given a rectangle and a legend
    dataTotal = []#initialises the total data list
    for d in dataList: dataTotal += d#loops through and adds to the data list
    
    xMin,xMax,xRange = dataAnalyse([ i[0] for i in dataTotal])#generates the minimum, maximum, and range for the x axis
    yMin,yMax,yRange = dataAnalyse([ i[1] for i in dataTotal])#generates the minimum, maximum, and range for the y axis
    yMin = 0; yRange = yMax#locks the y minimum to 0 for understandability
    xZoom,yZoom = rect[2]/xRange,rect[3]/yRange#calculates and stores the scale for x and y

    #draws the y axis
    pygame.draw.line(screen,white,rect[:2],dA(rect[:2],[0,rect[3]]))#draws the y axis line along the given rectangle
    x = rect[0]#saves the x position for the y axis
    for y in range(rect[1],rect[1]+rect[3],50):#loops from top to bottom of the y axis
        pygame.draw.line(screen,white,(x-2,y),(x+2,y))#draws a notch for the scale
        rY = yMax - (yMin + (y-rect[1])/yZoom)#determine the real y coordinate at this position
        centText(str(round(rY,1)),(x-30,y),white,smallFont)#draws this real y coordinate next to the graph

    #draws the x axis
    pygame.draw.line(screen,white,dA(rect[:2],rect[2:]),dA(rect[:2],[0,rect[3]]))#draws the x axis line along the given rectangle
    y = rect[1]+rect[3]#calculates and saves the y position for the x axis
    for x in range(rect[0],rect[0]+rect[2],50):#loops from left to right of the x axis
        pygame.draw.line(screen,white,(x,y-2),(x,y+2))#draws a notch for the scale
        rX = xMin + (x-rect[0])/xZoom#determine the real x coordinate at this position
        centText(str(round(rX/DAY_DURATION,2)),(x,y+10),white,smallFont)#draws this real x coordinate next to the graph
    centText("Time (Days)",[rect[0]+rect[2]/2,rect[1]+rect[3]+50])#draws the hardcoded title for the x axis

    for c,data in enumerate(dataList):#looping through each data list and its' index
        col = legend[c]#determines the colour from the legend
        pCo = None#initialises the previous coordinate
        for point in data:#looping through each point in the data
            x,y = tuple(point)#stores the x and y coordinates at each point
            dCo = [ (x - xMin)*xZoom + rect[0] , rect[1]+rect[3]-(y - yMin)*yZoom ]#converts the x and y into a drawn position within the plot
            if pCo != None: pygame.draw.line(screen,col,dCo,pCo)#if there is a previous position, draws a line from the previous position to the current in the relevant colour
            pCo = dCo[:]#sets the previous coordinate variable to the current coordinate
            
def drawLegend(legend):#draws the legend for a graph, given a dictionary of names and colours
    cCo = [650,100]#defines the legend position
    x,y = tuple(cCo)#stores the x and y coordinates
    for k in legend:#loops through the legend key
        re = [x,y,20,20]#determines and stores the rectangle of the legend key
        pygame.draw.rect(screen,legend[k],re)#draws the rectangle from the legend colour
        pygame.draw.rect(screen,white,re,2)#draws a border around the rectangle
        simpleText(k,(x+30,y))#draws the legend (species name) text next to the rectangle
        y += 30#incrememnts the y value so the legend draws down from the initial position

class Analytics:#The analytics class, which stores and runs the analytics and analytics menu
    def __init__(self,plants,animals,pTypes,aTypes):#initialises the analytics class, which the arrays for plants and animals by reference, as well as the list of plant and animal types
        self.plants,self.animals,self.pTypes,self.aTypes = plants,animals,pTypes,aTypes#stores the input paramters
        self.eTypes = aTypes + pTypes#defines entity types array as the sum of aniumal and plant types
        self.eStats = {}#initialises the entity statistics dictionary, stats are stored, list of (x,y) , (time,population)
        for name in self.eTypes: self.eStats[name] = []#initialises each categroy of the entity statistics dictionary
        self.legend = {"Tree" : brown , "Grass":[80,210,120] , "Fox":foxorange , "Rabbit" : [190,190,190]}#Defines the preset legend, matching species names to colours
        self.legendList = [self.legend[i] for i in self.eTypes]#forms a list in order of entity types using the legend dictionary
        self.globalTime = 0#initialises the global time class bound variable as 0
    def update(self,time):#updates the entity statistics dictionary with another data point
        for k in self.eStats: self.eStats[k].append([time,0])#adds another data point for each entity, initialising the time as the given time and the population to 0
        for e in self.plants+self.animals: self.eStats[e.name][-1][1] += 1#looping through all current entities, adding one to the respective population records for each
        self.globalTime = time#sets the global time variable to the current time
    def menu(self):#runs the analytics menu
        menuExit = False#initialises loop exit condition
        
        selection = DropDown(["All","Plants","Animals","Pair","Single"],[100,500,120,30],'Data',"All")#initialises the primary dropdown menu with its' selection options
        pSelection = [ DropDown(self.eTypes,[250+n*150,500,120,30],"Choice " + str(n),self.eTypes[n]) for n in range(2)]#initialises the pair(two) dropdown menus for the 'pair' option on the primary dropdown menu
        sSelection = DropDown(self.eTypes,[250,500,120,30],"Choice",self.eTypes[0])#initialises the single (one) dropdown menu for the 'single' option on the primary dropdown menu
        sTypes = self.eTypes[:]#initialises the selected entity types list with all, as the preset choice
        sLegend = [self.legend[i] for i in sTypes]#initialises the selected legend list, following the selected entity types list
        o = selection.output()#initialises the output choice storage variable
        selected = None#initialises the selected variable as None, as no menu is initially selected
        while not menuExit:#runs the loop with the menuExit exit condition
            mCo = pygame.mouse.get_pos()#obtains and stores the mouse position
            for ev in pygame.event.get():#runs through each queued event
                if ev.type == pygame.QUIT:#checks for a quit event
                    pygame.quit(); quit()#quits pygame and the python
                elif ev.type == pygame.MOUSEBUTTONDOWN:#checks for a down clicked mouse button
                    if ev.button == 1:#if the button was the left mouse button
                        if inRect(mCo,A_B_POS+B_DIM):#checks for the position of the mouse inside the analytics button
                            menuExit = True#sets the loop exit conditition to true
                        elif inRect(mCo,selection.rect):#checks if the mouse press was inside the primary dropdown menu
                            if selected != None: selected.selected = False#sets the previoiusly selected menu to not be selected any longer
                            selection.selected = True#sets the current selected menu to be selected 
                            selected = selection#sets selected to be the primary dropdown menu
                            selection.onPress(mCo)#runs the onPress function for the primary dropdown menu
                            o = selection.output()#stores the current output of the primary dropdown menu

                            #records the new selected entities
                            if o == "All": sTypes = self.eTypes[:]
                            elif o == "Plants": sTypes = self.pTypes[:]
                            elif o == "Animals": sTypes = self.aTypes[:]
                            elif o == "Pair":
                                sTypes = [i.output() for i in pSelection]
                            elif o == "Single":
                                sSelection.onPress(mCo)
                                sTypes = [sSelection.output()]
                            sLegend = [self.legend[i] for i in sTypes]#generates the new legend for the new selected entities
                            
                        elif o == "Pair":#checking if the mouse was on a pair selection dropdown menu instead
                            for i in pSelection:
                                if inRect(mCo,i.rect):#checks if the mouse is inside the dropdown menu rectangle
                                    if selected != None: selected.selected = False#sets the previoiusly selected menu to not be selected any longer
                                    i.selected = True#sets the current selected menu to be selected 
                                    selected = i#sets selected to be the current pair dropdown menu
                                    i.onPress(mCo)#runs the current pair dropdown menu's on click function
                                    sTypes = [i.output() for i in pSelection]#records the new selected entities from this pair
                                    sLegend = [self.legend[i] for i in sTypes]#generates the new legend for the new selected entities
                        elif o == "Single":#checking if the mouse was on a the single dropdown menu instead 
                            if inRect(mCo,sSelection.rect):
                                if selected != None: selected.selected = False#sets the previoiusly selected menu to not be selected any longer
                                sSelection.selected = True#sets the current selected menu to be selected 
                                selected = sSelection 
                                sSelection.onPress(mCo)#sets selected to be the single dropdown menu)
                                sTypes = [sSelection.output()]#generates the new legend for the new selected entity
                                sLegend = [self.legend[i] for i in sTypes]#generates the new legend for the new selected entity

            ##graphical display
            screen.fill(black)#fills the screen with black
            screen.blit(bSurface,(0,0))#draws the border surface to the screen
            if self.globalTime >= DAY_DURATION*0.5:#checks that the time is past 12:00pm on the first day
                selection.draw()#draws the primary dropdown menu
                if o == "Pair":
                    for i in pSelection: i.draw()#draws the pair dropdown menus if they are active
                elif o == "Single":
                    sSelection.draw()#draws the single dropdown menu if it is active
                
                plotSeveral([self.eStats[i] for i in sTypes],[100,100,500,300],sLegend)#runs the 'plotSeveral' function to plot the currently selected data
                tLegend = {}#initialises the temporary legend dictionary
                for e in sTypes: tLegend[e] = self.legend[e]#sets the temporary legend dictionary based on the currently selected data
                drawLegend(tLegend)#draws the temporary legend
            else:#if time is not past 12:00pm on the first day
                pygame.draw.rect(screen,white,[100,100,500,300],2)#draws the rectangle where the graph will be
                #draws text to tell the user the data will be ready at 12:00pm
                centText("Not Enough Data collected",[350,200],white)
                centText("Wait until 12:00pm",[350,300],white)
            
            screen.blit(aIcon,A_B_POS)#shows the analytics button sprite on the screen, enabling the user to toggle it off
            pygame.draw.rect(screen,black,A_B_POS + [30,30],2)#draws a border around the analytics button
            
            PDU()#updates the screen
            clock.tick(10)#makes the loop run at 10fps (as opposed to ~60 since it does not need to update the screen and events often)
   
class Model:#the model class, which stores the 3D models of all entities in the simulation
    def __init__(self,reLi,scale=1/5,baseRotation=0,altOrder=None):#initialises with the array of rectangular prisms, the scale of the model, the base model rotation, and the alternate ordering of the model, for view ordering
        nLi = []#iniitlaises the new rectangular prism array
        for re,c in reLi:#loops through the old rectangular prism array
            nLi.append([ [ i*scale for i in re] , c] )#calculates and transfers the old rectangular prism and colour to the new rectangular prism array
        tL = minCorner([i[0][:3] for i in nLi])#determines the top left / minimum corner of the model
        bR = maxCorner([nAdd(i[0][:3],i[0][3:]) for i in nLi])#determines the bottom right / maximum corner of the model
        self.size = nSub(bR,tL)#calculates and stores the size of the model using the minimum and maximum corner positions
        self.mLi = []#initialises the model rectangular prism array
        for re,c in nLi: self.mLi.append([ nSub(re[:3],tL)+re[3:] , c ])#generates the model rectangular prism array with the adjusted position
        self.ancAdjustment = [-i/2 for i in self.size[:2]] + [0]#generates the anchor adjustement to draw the model in the middle of some given position
        self.anchorPos = dD(self.size,[2,2])#genrates the anchor position of the model ( the xy centre)
        self.baseRotation = baseRotation#stores the base rotation of the model
        self.scale = scale#stores the scale of the model
        self.altOrder = altOrder#stores the alternate ordering of the model
        if self.altOrder != None:#if there is an alternate ordering
            self.altList = [self.mLi[ind] for ind in self.altOrder]#generates that rectangular prism list
        
    def draw(self,gPos,rotation):#draws the 3D model, given the rotation and the ground position
        p1 = rToD(nAdd(gPos,self.mLi[0][0][:3]))#generates the screen position of the first point in the model
        if inRect(p1,eSRect):#determines if that point is on screen, and only draws in that case
            rotation += self.baseRotation#adds the given rotation to that base rotation
            if self.altOrder != None and (rotation-self.baseRotation+0.12)%1 < 0.5: uLi = self.altList#determines if the alternate ordering should be used by the rotation, and if so uses the alternately ordered list
            else: uLi = self.mLi[:]#otherwises, uses the normal list
            
            rLi = []#initialises the rotatable rectangular prism array
            for re,c in uLi:#loops through the rectangular prism array
                
                #generates the  [position, side a, side b, side c] for the rotated rectangular prism
                p = vecRot(re[:2],rotation) + [re[2]]
                zA = re[5]
                a = vecRot([re[3],0],rotation) + [0]
                b = vecRot([0,re[4]],rotation) + [0]
                
                rLi.append([ [p,a,b,[0,0,zA]] , c ])#appends the rotated rectangular prism argument to the array

            #determines the offset position to draw the model from to draw it on the ground and around the given 'gPos'
            cA = dS(dD(dA(vecRot([self.size[0],0],rotation),vecRot([0,self.size[1]],rotation)),[2,2]) , self.anchorPos)
            nPos = dS(gPos[:2],cA) + [gPos[2]-self.size[2]]
            
            for re,c in rLi:#looping through the rotated rectangular prism array
                re = re[:]#copies re to not get side effect errors
                re[0] = nAdd(self.ancAdjustment,nAdd(re[0],nPos))#alters the first item of the list (the position) to draw it from the offset position
                drawRectPoly(re,c)#draws the rotated rectangular prism


#imports and initialises for all models
from Models import *
foxModel = Model(foxLi,0.20,foxBaseRotation,foxAltOrder)
rabbitModel = Model(rabbitLi,0.2,rabbitBaseRotation,rabbitAltOrder)
grassModel = Model(grassLi,0.2,grassBaseRotation,grassAltOrder)
treeModel = Model(treeLi,0.4,treeBaseRotation,treeAltOrder)

models = {"Fox":foxModel,"Rabbit":rabbitModel,"Grass":grassModel,"Tree":treeModel}#defubes the models dictionary with each animal
mKeys = list(models)#creates and stores a list of all model names

for k in mKeys:#generates a baby model, copying the paramters except for the scale, which is halved
    name = k.lower()
    models[k+"Baby"] = Model(eval(name+"Li"),round(models[k].scale/2,1),eval(name+"BaseRotation"),eval(name+"AltOrder"))


#======================
###RUNTIME SETUP
#======================

def generateBoardSprite():#pre-generates the board sprites, as well as the blit positions to make it show correctly at each possible zoom for run time effiency
    global add,zoom#makes add and zoom global variables, allowing the function to alter them as necessary for the graphics functions it uses
    bSList,sAPList = [],[]#initialises the board sprite array and screen anchor position array
    n = 0#initialises the counter
    loadingScreen(0,0)#shows the 0 progress loading screen
    for z in ZOOM_LEVELS:#loops through all zooom levels, as a sprite is needed for each
        
        loadingScreen(n,100*n/ZOOM_MAX_LEVEL)#runs a loading screen, with the progress given as the amount of loops divided by the total amount of loops needed.
        
        zoom = z#changes the zoom to the current level
        cos = [rToD(i) for i in [  [0,0,gZ],[gridW,0,gZ],[gridW,gridH,gZ],[0,gridH,gZ+1] ] ]#generates each of the bordering corners of the board, which show the most extreme drawing coordinates
        tL,bR = minCorner(cos,2),maxCorner(cos,2)#determines the top left and bottom right corners of these points
        
        loadingScreen(n,100*(n+0.3)/ZOOM_MAX_LEVEL)#draws the next loading screen, counting this as 0.3 of the progress before the next zoom stage
        
        size = dS(bR,tL)#calculates and stores the size of the sprite necessary
        add = dS(add,tL)#changes add to put the board squarely from (0,0) on a surface
        boardSprite = pygame.Surface(size, pygame.SRCALPHA, 32)#generates a new board sprite
        boardSprite.fill([0,0,0,0])#fills the new board sprite as a transparent layer, so the non used edges are transparent for the background
        showTablePers(boardSprite)#draws the table onto the board sprite
        
        loadingScreen(n,100*(n+0.9)/ZOOM_MAX_LEVEL)#shos the next loading screen, counting this as 0.9 of the progress before the next zoom stage
        
        sAPos = dToR([0,0],gZ)+[gZ]#calculates the screen anchor position for the current zoom level
        bSList.append(boardSprite)#appends the board sprite to the board sprite array
        sAPList.append(sAPos)#appends the screen anchor position to the array of screen anchor positions

        n += 1#increments the counter
        
    return bSList,sAPList#returns the arrays of board sprites and screen anchor positions

 
def runSim(settings):#runs a simulation given a settings record
    global zoom,add,table,tableCol,tableWP,animals,plants#makes the neccessary variables global to allow interaction between function scope variables
    
    bType = settings.generateBType()#returns the biome type from the settings record
    table = [[tileData(terrainGenerationFunction(x,y),bType)[0] for x in range(gridW)] for y in range(gridH)]#generates the table of tile IDs from the formula function
    tableCol = [[tileData(terrainGenerationFunction(x,y),bType)[1] for x in range(gridW)] for y in range(gridH)]#generates the table of tile colours from the formula function and the biome type
    tableWP = genPath()#generates the table water pathfinding table for the generated table

    timeMult = 2#defines a time multiplier for all
    
    add = [0,0]#resets the camera offset to 0
    boardSpriteList,sAPosList = generateBoardSprite()#generates the board sprites and anchor positions for each zoom level
    zoomLevel = 7#stores the initial zoom level
    zoom = ZOOM_LEVELS[zoomLevel]#stores the zoom value
    add = setView([gridW//2,gridH//2,gZ],sCent)#sets the initial camera position to have the middle of the grid in the middle of the screen
    
    gameExit = False#initialises the loop exit condition
        
    animals,plants = settings.generateEntities()#generates the arrays of animals and plants from the settings class

    actionDi = {pygame.K_q:Animal.possessDrink,pygame.K_e:Animal.possessEat,pygame.K_z:Animal.toggleView}#defines the action dictionary, of which keys activate which functions when possessing a creature

    timeMultiplier = 1#defines the current time multiplier
    T_M_VALUES = [0,1]#defines all possible time multiplier values

    possessed = None#initialises the possessed variable, storing which creature is being possessed

    background = GradBackground((20,None,None) , (None,None,90) )#initialises the gradient background for the day night cycle
    analytics = Analytics(plants,animals,settings.plantTypes,settings.animalTypes)#initialises the analytics function

    dTicks = 0#initialises the day ticks as 0
    days = 0#initialises the day counter as 0
    while not gameExit:#runs the loop with the exit condition 'gameExit'
        keys = pygame.key.get_pressed()#generates and stores an array of whether or not any given key is pressed
        mCo = pygame.mouse.get_pos()#generates and stores the mouse position
        
        storeCo = dToR(mCo,gZ)#generates the in game position the mouse cursor is currently over (at the global Z level)
        for ev in pygame.event.get():#obtains the list of all queued events
            if ev.type == pygame.QUIT:#checks for the quit event
                pygame.quit(); quit()#quits pygame and python
            elif ev.type == pygame.MOUSEBUTTONDOWN:#checks for a down mouse click
                if ev.button == 1:#checks if the mouse button was a left click
                    if inRect(mCo,A_B_POS+B_DIM): analytics.menu()#if the analytics button is pressed, runs the analytics menu
                    elif inRect(mCo,TM_B_POS+B_DIM):#if the time multiplier button was pressed
                        tMIndex = T_M_VALUES.index(timeMultiplier)#determines the index of the current time multiplier
                        tMIndex = (tMIndex + 1)%len(T_M_VALUES)#increments and rolls over the index of the time multiplier
                        timeMultiplier = T_M_VALUES[tMIndex]#sets the new time mulitplier to the time multiplicity at the new index
                    elif inRect(mCo,E_B_POS+B_DIM): gameExit = True#if the 'X' button is pressed, activates the loop exit condition
                    else:#if it was none of these buttons, attempts to find an animal to possess
                        rCo = [int(i) for i in dToR(mCo,gZ)]#determines what tile the user would be clicking on

                        #searches for any animals on that specific tile
                        lEntities = chunkSearch(rPTC(rCo))
                        for entity in lEntities:
                            if entity.eType == "Animal":
                                if dF(entity.pos) == rCo:
                                    if DEBUG: entity.giveReadout()#gives the readout if debug mode is on
                                    if possessed != None: possessed.possessed = False#sets the previously possessed entity flag to inactive
                                        
                                    possessed = entity#sets possessed to be the newly possessed entity
                                    entity.possessed = True#sets the entity possessed flag to be active
                                
                elif ev.button in [4,5]:#checks if the mouse button was scroll wheel up or down
                    if ev.button == 4: zoomLevel += 1#increments the zoom level for a scroll wheel up
                    else: zoomLevel -= 1#decrements the zoom level for a scroll wheel down
                    zoomLevel = limit(zoomLevel,ZOOM_MAX_LEVEL-1,0)#limits the zoom level between 0 and the maximum
                    zoom = ZOOM_LEVELS[zoomLevel]#sets the zoom value to the appropiate zoomList index
            elif ev.type == pygame.KEYDOWN:#checks for a keydown event
                if ev.key in actionDi:#checks through the possessed action dictionary keys
                    if possessed != None:
                        actionDi[ev.key](self=possessed)#runs the action given by the pressed key with the possessed creature
                elif ev.key == pygame.K_x:#checks if the key pressed x
                    #unpossesses the possessed if there is one currently
                    if possessed != None:
                        possessed.possessed = False
                    possessed = None

        if possessed != None and timeMultiplier != 0:#enables possession movement is there is a possessed animal and time is running through the moveDi dictionary
            cha = [0,0]#initialise the change vector variable to 0
            for k in moveDi:#looping through the keys of moveDi
                if keys[k]:#if the key is pressed
                    cha = dA(cha,moveDi[k])#adds the related vector the cha vector
            if cha != [0,0]:#if there is a change
                possessed.move(cha)#moves by the change
        if possessed != None and possessed.possessedView == 1:#if something is possessed and it has view centering enabled
            add = setView(possessed.pos+[gZ],sCent)#centers the view to the possessed creature
        else:#otherwise
            add = setView(storeCo+[gZ],mCo)#centres the stored position before to the mouse position, meaning that where your mouse is pointing will stay constant as you zoom
            for k in kDi:#using the kDi dictionary, enables camera movement with WASD
                if keys[k]: add = dA(add,dM(kDi[k],[10]*2))#changes the camera position if the related key is pressed
            
        if timeMultiplier != 0:#if time is running (not 0)
            for c1 in reversed([c for c,animal in enumerate(animals) if not animal.update()]): del animals[c1]#updates and deletes dead animals
            for c1 in reversed([c for c,plant in enumerate(plants) if not plant.update()]): del plants[c1]#updates and deletes dead plants
            if dTicks%AGE_T_INTERVAL == 0:#if the day ticks are cleanly divisible by the age time interval
                for i in animals + plants: i.ageAdd(AGE_ADD)#ages all animals and plants
                analytics.update(dTicks+days*DAY_DURATION)#updates the population analytics
            if dTicks%RANDOM_T_INTERVAL == 0:#if the day ticks are cleanly divisible by the random ticks interval
                for i in animals + plants: i.randomTick()#runs the random tick function for each entity
        
        background.update(dTicks)#updates the gradient (day-night cycle) with the day ticks
        
        if not (keys[pygame.K_LALT] or keys[pygame.K_RALT]):#if the alt key is not pressed
            screen.blit(boardSpriteList[zoomLevel],rToD(sAPosList[zoomLevel]))#blits the appropiate zoomed map at the related blitting position, using the stored anchor position and the rToD graphics function
            eList = sorted(animals + plants,key= lambda x : x.bStore)#entity list, sorted by 'b' (as in y = x + b), sorting the view ordering
            for e in eList: e.draw()#draws each entity in the list order
            clock.tick(20)#attempts to runs the loop 20 times per second
        else:#if they alt key is pressed
            centText('>'*3,sCent,white,bigfont)#draws ">>>" in the middle of the screen in white
            le0 = (dTicks//100)%3; le1 = 2 - le0#determines the length of the white ones to have a rotating grey one
            centText(le0*' '+'>'+le1*' ',sCent,darkgray,bigfont)#draws one '>', with appropiate spaces to draw the '>' at the correct place, in grey for differentiation
            clock.tick(0)#sets the clock to an unlimited spped
            
        screen.blit(bSurface,(0,0))#blits the border surface to the screen

        screen.blit(aIcon,A_B_POS)#blits the analytics menu sprite to the screen
        pygame.draw.rect(screen,black,A_B_POS + [30,30],2)#draws the analytics menu button border on the screen

        pygame.draw.rect(screen,white,TM_B_POS + [30,30])#draws the time multiplier button background as white
        pygame.draw.rect(screen,black,TM_B_POS + [30,30],2)#draws the time multiplier button border as black
        centText(str(timeMultiplier)+'x',TM_B_MIDPOINT,black)#draws the multiplier + 'x' into the centre of the time multiplier button 
        

        pygame.draw.rect(screen,white,E_B_POS + [30,30])#draws the exit button background as white
        pygame.draw.rect(screen,black,E_B_POS + [30,30],2)#draws the exit button border as black
        centText('X',E_B_MIDPOINT,black)#draws an 'X' into the centre of the exit button
        
        if possessed != None:#if an animal is possessed
            if not possessed.alive: possessed = None#if the animal is dead, stop possessing it
            else: possessed.possessionMenu()#otherwise, run the possession menu
        
        simpleText("Day " + str(days) + ", " + stTime(dTicks),co=dA([50,0],E_B_POS))#draws the day and time onto the top left of the screen
        
        PDU()#updates the screen
        if timeMultiplier != 0:#if time is running (not 0)
            dTicks += timeMult#increments the dayTicks by the base time multiplier
            if dTicks >= DAY_DURATION:#if dTicks is greater than the duration of one day
                days += 1#increments the days counter
                dTicks = dTicks - DAY_DURATION#sets 'dTicks' to be the different between 'dTicks' and the day duration
        



def runPreset():#runs the preset simulation
    global zoom,add,table,tableCol,tableWP,animals,plants,boardSprite#makes the neccessary variables global to allow interaction between function scope variables
    settings = SimSettings(*importSettings("Presets\\Life of a Fox.txt"))#imports setting from a prechosen settings file
    bType = settings.generateBType()#returns the biome type from the settings record
    table = [[tileData(terrainGenerationFunction(x,y),bType)[0] for x in range(gridW)] for y in range(gridH)]#generates the table of tile IDs from the formula function
    tableCol = [[tileData(terrainGenerationFunction(x,y),bType)[1] for x in range(gridW)] for y in range(gridH)]#generates the table of tile colours from the formula function and the biome type
    tableWP = genPath()#generates the table water pathfinding table for the generated table

    timeMult = 2#defines a base time multiplier
    
    add = [0,0]#resets the camera offset to 0
    boardSpriteList,sAPosList = generateBoardSprite()#generates the board sprites and anchor positions for each zoom level
    zoomLevel = 7#stores the initial zoom level
    zoom = ZOOM_LEVELS[zoomLevel]#stores the zoom value
    add = setView([gridW//2,gridH//2,gZ],sCent)#sets the initial camera position to have the middle of the grid in the middle of the screen
    
    gameExit = False#initialises the loop exit condition
        
    animals,plants = settings.generateEntities()#generates the arrays of animals and plants from the settings class
    
    actionDi = {pygame.K_q:Animal.possessDrink,pygame.K_e:Animal.possessEat,pygame.K_z:Animal.toggleView}#defines the action dictionary, of which keys activate which functions when possessing a creature

    timeMultiplier = 1#defines the current time multiplier
    T_M_VALUES = [0,1]#defines all possible time multiplier values

    background = GradBackground((20,None,None) , (None,None,90) )#initialises the gradient background for the day night cycle
    analytics = Analytics(plants,animals,settings.plantTypes,settings.animalTypes)#initialises the analytics function

    #preset possession setup
    possessed = animals[0]#sets the possessed animal to be the first one, which always be a lone fox, as given by the settings file
    possessed.toggleView()#sets the view to be centered on the possessed animal by default
    possessed.possessed = True#sets the possessed animal's possession flag to be active
    possessed.age = 1#sets the possessed animal to be one day old
    possessed.quest = 0#initialises the possessed animal's quest variable at 0
    possessed.aMenu = analytics#sets a variable bound to the possessed animal to equal the possession menu, so the possessed animal may access the analytics data
    possessed.pShowLen = 4#sets the possessed animal's pShowLen variable to be 4 instead of 5, so the possession menu does not include the exit possession button, as the user cannot quit possession in a preset
    pText = ''#sets the possession float text to be empty 
    
    dTicks = 0#initialises the day ticks as 0
    days = 0#initialises the day counter as 0
    while not gameExit:#runs the loop with the exit condition 'gameExit'
        keys = pygame.key.get_pressed()#generates and stores an array of whether or not any given key is pressed
        mCo = pygame.mouse.get_pos()#generates and stores the mouse position
        
        storeCo = dToR(mCo,gZ)#generates the in game position the mouse cursor is currently over (at the global Z level)
        for ev in pygame.event.get():#obtains the list of all queued events
            if ev.type == pygame.QUIT:#checks for the quit event
                pygame.quit(); quit()#quits pygame and python
            elif ev.type == pygame.MOUSEBUTTONDOWN:#checks for a down mouse click
                if ev.button == 1:#checks if the mouse button was a left click
                    if inRect(mCo,A_B_POS+B_DIM): analytics.menu()#if the analytics button is pressed, runs the analytics menu
                    elif inRect(mCo,TM_B_POS+B_DIM):#if the time multiplier button was pressed
                        tMIndex = T_M_VALUES.index(timeMultiplier)#determines the index of the current time multiplier
                        tMIndex = (tMIndex + 1)%len(T_M_VALUES)#increments and rolls over the index of the time multiplier
                        timeMultiplier = T_M_VALUES[tMIndex]#sets the new time mulitplier to the time multiplicity at the new index
                    elif inRect(mCo,E_B_POS+B_DIM): gameExit = True#if the 'X' button is pressed, activates the loop exit condition
                                
                elif ev.button in [4,5]:#checks if the mouse button was scroll wheel up or down
                    if ev.button == 4: zoomLevel += 1#increments the zoom level for a scroll wheel up
                    else: zoomLevel -= 1#decrements the zoom level for a scroll wheel down
                    zoomLevel = limit(zoomLevel,ZOOM_MAX_LEVEL-1,0)#limits the zoom level between 0 and the maximum
                    zoom = ZOOM_LEVELS[zoomLevel]#sets the zoom value to the appropiate zoomList index
            elif ev.type == pygame.KEYDOWN:#checks for a keydown event
                if ev.key in actionDi:#checks through the possessed action dictionary keys
                    if possessed != None:
                        actionDi[ev.key](self=possessed)#runs the action given by the pressed key with the possessed creature

        if possessed != None and timeMultiplier != 0:#enables possession movement is there is a possessed animal and time is running through the moveDi dictionary
            cha = [0,0]#initialise the change vector variable to 0
            for k in moveDi:#looping through the keys of moveDi
                if keys[k]:#if the key is pressed
                    cha = dA(cha,moveDi[k])#adds the related vector the cha vector
            if cha != [0,0]:#if there is a change
                possessed.move(cha)#moves by the change
        if possessed != None and possessed.possessedView == 1:#if something is possessed and it has view centering enabled
            add = setView(possessed.pos+[gZ],sCent)#centers the view to the possessed creature
        else:#otherwise
            add = setView(storeCo+[gZ],mCo)#centres the stored position before to the mouse position, meaning that where your mouse is pointing will stay constant as you zoom
            for k in kDi:#using the kDi dictionary, enables camera movement with WASD
                if keys[k]: add = dA(add,dM(kDi[k],[10]*2))#changes the camera position if the related key is pressed 

        if timeMultiplier != 0:#if time is running (not 0)
            for c1 in reversed([c for c,animal in enumerate(animals) if not animal.update()]): del animals[c1]#updates and deletes dead animals
            for c1 in reversed([c for c,plant in enumerate(plants) if not plant.update()]): del plants[c1]#updates and deletes dead plants
            if dTicks%AGE_T_INTERVAL == 0:#if the day ticks are cleanly divisible by the age time interval
                for i in animals + plants: i.ageAdd(AGE_ADD)#ages all animals and plants
                analytics.update(dTicks+days*DAY_DURATION)#updates the population analytics
            if dTicks%RANDOM_T_INTERVAL == 0:#if the day ticks are cleanly divisible by the random ticks interval
                for i in animals + plants: i.randomTick()#runs the random tick function for each entity
        
        background.update(dTicks)#updates the gradient (day-night cycle) with the day ticks
        
        if not (keys[pygame.K_LALT] or keys[pygame.K_RALT]):#if the alt key is not pressed
            screen.blit(boardSpriteList[zoomLevel],rToD(sAPosList[zoomLevel]))#blits the appropiate zoomed map at the related blitting position, using the stored anchor position and the rToD graphics function
            eList = sorted(animals + plants,key= lambda x : x.bStore)#entity list, sorted by 'b' (as in y = x + b), sorting the view ordering
            for e in eList: e.draw()#draws each entity in the list order
            clock.tick(20)#attempts to runs the loop 20 times per second
        else:#if they alt key is pressed
            centText('>'*3,sCent,white,bigfont)#draws ">>>" in the middle of the screen in white
            le0 = (dTicks//100)%3; le1 = 2 - le0#determines the length of the white ones to have a rotating grey one
            centText(le0*' '+'>'+le1*' ',sCent,darkgray,bigfont)#draws one '>', with appropiate spaces to draw the '>' at the correct place, in grey for differentiation
            clock.tick(0)#sets the clock to an unlimited speed
              
        screen.blit(bSurface,(0,0))#blits the border surface to the screen

        screen.blit(aIcon,A_B_POS)#blits the analytics menu sprite to the screen
        pygame.draw.rect(screen,black,A_B_POS + [30,30],2)#draws the analytics menu button border on the screen

        pygame.draw.rect(screen,white,TM_B_POS + [30,30])#draws the time multiplier button background as white
        pygame.draw.rect(screen,black,TM_B_POS + [30,30],2)#draws the time multiplier button border as black
        centText(str(timeMultiplier)+'x',TM_B_MIDPOINT,black)#draws the multiplier + 'x' into the centre of the time multiplier button 

        pygame.draw.rect(screen,white,E_B_POS + [30,30])#draws the exit button background as white
        pygame.draw.rect(screen,black,E_B_POS + [30,30],2)#draws the exit button border as black
        centText('X',E_B_MIDPOINT,black)#draws an 'X' into the centre of the exit button
        
        if possessed != None:#if there is still a possessed animal
            if not possessed.alive:#if the possessed animal died
                pText = "You died from " + possessed.cause#update the float text to state the cause of death
                possessed = None#sets possessed to none
            else:#if the possessed animal is still alive
                possessed.possessionMenu()#runs the possessed animal's possession animal
                possessed.questMenu()#runs the possessed animal's quest menu
        
        simpleText("Day " + str(days) + ", " + stTime(dTicks),co=dA([50,0],E_B_POS))#draws the day and time onto the top left of the screen
        if pText != '': simpleText(pText,P_T_POS)#if there is possession float text, draws it in the bottom left above at the given position
        
        PDU()#updates the screen
        if timeMultiplier != 0:#if time is running (not 0)
            dTicks += timeMult#increments the dayTicks by the base time multiplier
            if dTicks >= DAY_DURATION:#if dTicks is greater than the duration of one day
                days += 1#increments the days counter
                dTicks = dTicks - DAY_DURATION#sets 'dTicks' to be the different between 'dTicks' and the day duration


class SimSettings:#The simulation settings record, which stores all settings for any given simulation
    def __init__(self,terrainType,plantDataList,animalDataList,simName):#initialises with terrain type, animal and plant data lists, and the simulation name
        self.terrainType,self.animalDataList,self.plantDataList,self.simName = terrainType,animalDataList,plantDataList,simName#stores all attributes class bound

        #converts the attribute lists taken from the menus to the attribute dictionaries taken by Plant records
        self.plantList = plantDataList[:]#makes a copy of the plantDataList
        for pDict in self.plantList:#loops through the plant list
            for c,i in enumerate(PLANT_INPUT_FIELDS):#loops through the different plant input fields index and type
                pDict[i] = PLANT_INPUT_TYPES[c](pDict[i])#type casts with the relevant type from 'PLANT_INPUT_TYPES' to the data from the initial plant dictionary

        #converts the attribute lists taken from the menus to the attribute dictionaries taken by Plant records   
        self.animalList = animalDataList[:]#makes a copy of the animalDataList
        for aDict in self.animalList:#loops through the animal list
            for c,i in enumerate(ANIMAL_INPUT_FIELDS):#loops through the different animal input fields index and type
                aDict[i] = ANIMAL_INPUT_TYPES[c](aDict[i])#type casts with the relevant type from 'PLANT_INPUT_TYPES' to the data from the initial plant dictionary

        #generates the animal type and initial population arrays
        self.animalTypes,self.animalIPop = [],[]#initialises the animal type and initial population arrays as empty
        for aDict in self.animalList:#looping through each animal
            self.animalTypes.append(aDict["Species"])#appending this animal's species to the animal types array
            self.animalIPop.append(aDict["InitialPopulation"])#appending this animal's initial population to the animal initial population array

        #generates the plant type and initial abundance arrays
        self.plantTypes,self.plantAbundance = [],[]#initialises the plant type and initial abundance arrays as empty
        for pDict in self.plantList:#looping through each plant
            self.plantTypes.append(pDict["Species"])#appending this plant's species to the animal types array
            self.plantAbundance.append(pDict["Abundance"])#appending this plant's initial abundance to the plant initial abundance array
            
    def generateBType(self):#returns the terrain biome type
        return TERRAIN_TYPES.index(self.terrainType)
    def generateEntities(self):#generates the initial arrays of animals and plants
        animals = []#initialises the animals array
        for c,t in enumerate(self.animalList):#loops through the animal type data list
            for n in range(self.animalIPop[c]//POPULATION_SCALE):#loops for the initial population size
                animals += [Animal(t)]#generates a new animal with the related dictionary reference
                
        plants = []#initialises the plants array
        for c,t in enumerate(self.plantList):#loops through the plant type data list
            for n in range(self.plantAbundance[c]//POPULATION_SCALE):#loops for the initial abundance
                plants += [Plant(t)]#generates a new plant with the related dictionary reference
                
        return animals,plants#returns the animals and plants array
    def exportSettings(self):#exports its' settings a text file
        fileName = "PastSims\\"+self.simName + ".txt"#determines and stores the file name, given by the folder it will be in and the simulation name
        txt = self.simName+"\n"+self.terrainType + '\n'#initialises the text content with the simulation name and terrain type
        txt += "Animals\n=\n"#adds the Animals section to the text content
        for i in self.animalDataList:#loops through the different animal data
            for i1 in ANIMAL_INPUT_FIELDS:#loops through the animal fields
                txt += str(i[i1]) + '\n'#adds the string representation of each field to the file, and a newline character
            txt += "=" + '\n'#adds the '=' to signifiy the end of those animal attributes
            
        txt += "Plants\n=\n"#adds the Plants section to the text content
        for i in self.plantDataList:#loops through the different plant data
            for i1 in PLANT_INPUT_FIELDS:#loops through the plant fields
                txt += str(i[i1]) + '\n'#adds the string representation of each field to the file, and a newline character
            txt += "=" + '\n'#adds the '=' to signifiy the end of those plant attributes

        with open(fileName,'w') as f: f.write(txt)#writes the text to the file
        addToDirectory(self.simName + ".txt")#adds the new text file to the previous simulations directory

def importSettings(fileName):#import settings from a given file
    with open(fileName,'r') as f: txt = f.read().splitlines()#imports text from the file and splits it into a list of lines
    simName = txt[0]#determines and stores the simulation name from the first line
    terrain = txt[1]#determines and stores the simulation name from the second line
    
    plantsLine = txt.index("Plants")#determines when the plant records start by indexing the line that has only "Plants"
    
    animalLines = txt[3:plantsLine]#generates and stores the lines that include animal defintions
    animals = []#initialise the animals list
    newAnimal = None#initialise the 'newAnimal' variable
    for l in animalLines:#loops through the animal definition lines
        if l == '=':#checks '=' as '=' happens when a new animal is starting
            if newAnimal != None: animals.append(newAnimal)#if there was a previous new animal, add it to the list of animals
            newAnimal = []#reinitialise the new animal list
        else: newAnimal.append(l)#if it is a normal line, simply adds the line to the list
    for c,animal in enumerate(animals):#looping through each generated animal list and index
        newAnimal = {}#initialises a new animal dictionary
        for c1,i in enumerate(animal):#looping through the index and item of this animal data
            newAnimal[ANIMAL_INPUT_FIELDS[c1]] = i#typecasts the data by index into the new animal dictionary
        animals[c] = newAnimal#sets the index of the animal list to the new animal dictionary
        
    plantLines = txt[plantsLine+1:]#generates and stores the lines that include plant defintions
    plants = []#initialise the plants list
    newPlant = None#initialise the 'newPlant' variable
    for l in plantLines:#loops through the plant definition lines
        if l == '=':#checks '=' as '=' happens when a new plant is starting
            if newPlant != None: plants.append(newPlant)#if there was a previous new animal, add it to the list of plants
            newPlant = []#reinitialise the new plant list
        else: newPlant.append(l)#if it is a normal line, simply adds the line to the list
    for c,plant in enumerate(plants):#looping through each generated plant list and index
        newPlant = {}#initialises a new plant dictionary
        for c1,i in enumerate(plant):#looping through the index and item of this plant data
            newPlant[PLANT_INPUT_FIELDS[c1]] = i#typecasts the data by index into the new plant dictionary
        plants[c] = newPlant#sets the index of the plant list to the new animal dictionary
    
    output = [terrain,plants,animals,simName]#records the input in the order of parameters for a settings record initialisation
    return output#returns the output

def addToDirectory(fileName):#adds a given filename to the past simulation directory
    with open("PastSims\\directory.txt",'a') as f:
        f.write("\n"+fileName) 
def importDirectory():#imports all filenames from the past simulation directory
    with open("PastSims\\directory.txt",'r') as f:
        txt = f.read().splitlines()
    txt = ["PastSims\\"+i for i in txt]
    return txt
def deleteSettings(c):#deletes a certain setting file as well as the directory entry
    #deletes line from directory
    with open("PastSims\\directory.txt",'r') as f:
        txt = f.read().splitlines()
    i = txt[c]
    del txt[c]
    with open("PastSims\\directory.txt",'w') as f:
        f.write('\n'.join(txt))
        
    remove("PastSims\\"+i)#deletes the file
    
    


    
lBSize = [600,90]#defines the loading bar size
lBRect = [sCent[0]-lBSize[0]/2 , sCent[1]-80] + lBSize#calculates and defines the loading bar rectangle, centering it on the screen

colourDisplay = pygame.Surface(dA(lBSize,[90,0]), pygame.SRCALPHA, 32)#initialises the loading bar rectangle
colourDisplay.fill([0,0,0,20])#fills the loading bar rectangle with black at 20 opacity (20/255)
for x in range(-90,lBSize[0]+90,30): pygame.draw.line(colourDisplay,[0,0,0,30],[x,0],[x+lBSize[1],lBSize[1]],15)#draws diagonal lines through the surface

aboveTextPos = [sCent[0] , lBRect[1]-12]#calculates and stores the above text position
belowTextPos = [sCent[0] , lBRect[1]+lBRect[3]+12]#calculates and stores the below text position

tSize = [300,90]#defines the text size
tRect = [sCent[0]-tSize[0]/2 , sCent[1]-280] + tSize#calculates and defines the title text rectangle, centering it horizontally on the screen
tCent = [tRect[n]+tRect[n+2]/2 for n in range(2)]#calculates and stores the centre of the title text rectangle

def loadingScreen(ticks,percent):#draws the loading screen, given the ticks and the percentage completed
    keys = pygame.key.get_pressed()#generates and stores an array of whether or not any given key is pressed
    mCo = pygame.mouse.get_pos()#generates and stores the mouse position

    #updates the event listener, to enable the user to quit and pygame to not crash
    for ev in pygame.event.get():#obtains the list of all queued events
        if ev.type == pygame.QUIT:#checks for the quit event
            pygame.quit(); quit()#quits pygame and python

    col = [50-50*cos((0/101)),50+50*cos(0/863),50+50*sin(0/207+2)]#calculates the background colour
    screen.fill(col)#fills the background with this colour
            
    screen.blit(bSurface,(0,0))#draws the border onto the screen
    pygame.draw.rect(screen,green,lBRect)#draws a green background for the loading bar
    screen.blit(colourDisplay,dA(lBRect[:2],[-90+(ticks*5)%90,0]))#draws the loading bar texture on the loading bar, moving to the right as the 'ticks' variable increases
    pygame.draw.rect(screen,col,dA(lBRect[:2],[-90,0])+[90,90])#draws a rectangle hiding the loading bar going over the left side as it moves
    pygame.draw.rect(screen,col,dA(lBRect[:2],[lBRect[2],0])+[90,90])#draws a rectangle hiding the loading bar going over the right side as it moves
    le = lBSize[0]*percent/100#calculates and stores the loading bar length
    pygame.draw.rect(screen,col,[lBRect[0]+le,lBRect[1],lBRect[2]-le,lBRect[3]])#draws over the rest of the loading bar, to show only the loading section
    pygame.draw.rect(screen,white,lBRect,2)#draws a border around the loading bar

    centText("Watering the Grass",aboveTextPos,white)#draws a random float text above the loading bar
    centText(str(int(percent))+'%'+ " complete",belowTextPos,white)#draws the percentage completion below the loading bar

    pygame.draw.rect(screen,black,tRect)#draws a black background for the title text
    pygame.draw.rect(screen,white,tRect,2)#draws a white background for the title text
    centText("Eco Sim",tCent,white,bigfont)#draws the title centered in the title text rectangle

    PDU()#updates the screen
    

def lineText(text,co,colour=white,lineSize=30,font = myFont):#draws lines of text, seperated by the newline character '\n'
    for c,line in enumerate(text.splitlines()):#splits the text by index and line
        simpleText(line,dA(co,[0,c*lineSize]),colour,font)#calculates and draws the text at the calculated position

def splitText(text,lineLength):#splits text into by the newline character and by a maximum line length
    words = text.split(' ')#splits the text into words
    wordsAmount = len(words)#calaculates and stores the amount of words
    c,cLen = 0,0#initialises the counter and current length variables
    lines,line = [],''#initialises the lines and line variables
    while c < wordsAmount:#exit condition of going over the amount of words
        nextWord = words[c]#determines and stores the next word by index
        if len(nextWord) + cLen > lineLength:#determines if the next word will push the current line length over the limit
            lines.append(line)#appends the current line to the lines array
            line = ''#resets the current line variable to an empty string
            line += nextWord + ' '#add the next word to the next line
            cLen = len(nextWord) + 1#resets the current length variable to the length of the next word
        elif '\n' in nextWord:#checks for a newline character in the next word
            nextWord.replace('\n','')#removes \n from the word
            line += nextWord#adds the next word to the current line=
            lines.append(line)#appends the current line to the lines array
            line = ''#resets the current line variable to an empty string
            cLen = 0#resets the current length variable
        else:#a normal case
            line += nextWord + ' '#adds the next word as well as a space to the next line
            cLen += len(nextWord) + 1#updates the current line length to the new amount
        c += 1#increments the counter
    lines.append(line)#adds the final line to the array of lines
    return '\n'.join(lines)#returns all lines joined by '\n' characters

class MenuButton:#main menu button class, links to a submenu which shows when clicked
    mType = "M1"#defines the menu type as "M1", a menu class which always shows and is a main button
    def __init__(self,text,y,subMenu=None):#initialises the menu button class
        self.rect = [ 10, y, 200, 40 ]
        self.cent = [ 10+100 , y+20 ] 
        self.visibile, self.selected = True, False
        self.text,self.subMenu = text, subMenu
    def onPress(self,mCo,button=1):#takes the menu position, and runs process for being clicked on
        if self.subMenu != None: self.subMenu.visibile = True
        self.selected = True
        return self
    def offPress(self):#runs for the process for the menu being clicked off
        if self.subMenu != None:
            self.subMenu.visibile = False
            self.subMenu.offPress()
        self.selected = False
    def onScroll(self,di): pass#runs the process for the menu being scrolled on, given the scroll direction
    def onKey(self,ev):#runs the process for the menu being typed on 
        if self.subMenu != None: self.subMenu.onKey(ev)
    def draw(self):#runs the process for the menu being drawn
        mP = pygame.mouse.get_pos()
        pygame.draw.rect(screen,[90]*3 if inRect(mP,self.rect) else black,self.rect)
        pygame.draw.rect(screen,blue if self.selected else white,self.rect,2)
        centText(self.text,self.cent)

class NewTrial:#New Trial class, allows the user to create a new trial/simulation customised paramters
    mType = "M0"#defines the menu type as "M0", a menu class one below the menu buttons
    def __init__(self):#initialises the new trial menu class
        self.rect = [ 250 , 60 , 600 , 630 ]
        self.rect1 = [ 250 , 60 , 200 , 630 ]
        self.subSelected = self.listSelected = None
        self.visibile = False
        self.subMenus = [
DropDown(TERRAIN_TYPES,[260,80+10,180,30],"Terrain"),
ItemList([260,250,180,120],AddNewPlant,"Plants",self,"Species"),
ItemList([260,410,180,120],AddNewAnimal,"Animals",self,"Species"),
TextField([260,570,180,30],label="Name"),
EventButton([260,640,180,40],text="Create",ev=self.createNewSim)
]   
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        for i in self.subMenus:
            if inRect(mCo,i.rect):
                i.selected = True
                if self.subSelected != None and self.subSelected != i:
                    if i in self.subMenus and self.subSelected.mType == "An":
                        self.listSelector()
                    self.subSelected.selected = False
                    self.subSelected.offPress()
                i.onPress(mCo)
                self.subSelected = i 
    def offPress(self):
        if self.subSelected != None:
            self.subSelected.selected = False
            self.subSelected.offPress()
        self.subSelected = None
    def onScroll(self,di):
        for i  in self.subMenus:
            if inRect(mCo,i.rect):
                i.onScroll(di)
    def onKey(self,ev):
        if self.subSelected != None: self.subSelected.onKey(ev)
    def draw(self):
        pygame.draw.rect(screen,black,self.rect1)
        pygame.draw.rect(screen,white,self.rect1,2)
        for i in self.subMenus: i.draw()
    def listSelector(self,new=None):
        if self.listSelected != None: del self.subMenus[-1]
        self.listSelected = new
        if new != None: self.subMenus.append(new)
    def createNewSim(self):
        data = [i.output() for i in self.subMenus[:4]]
        if not ( (None in data) or '' in data or [] in data):
            settings = SimSettings(*data)
            settings.exportSettings()
            runSim(settings)
            self.pastSim.items = importDirectory()
            
class PastSims:#Past Simulations class, which allows the user to load or delete previous simulations
    mType = "M0"#defines the menu type as "M0", a menu class one below the menu buttons
    def __init__(self):#initialises the past sims button class
        self.rect = [ 250 , 60 , 200 , 630 ]
        self.visibile,self.subSelected = False, None
        self.items = importDirectory()
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        x,y = tuple(self.rect[:2])
        toDel = None
        for c,i in enumerate(self.items):
            labelText = i[9:-4]
            simpleText(labelText,(x+4,y+1))
            re = [x+4,y+25,20+40,20]#'L'
            if inRect(mCo,re):
                settings = SimSettings(*importSettings(i))
                runSim(settings)
            re = [x+4+170,y+25,20,20]# 'X'
            if inRect(mCo,re): toDel = c
            y += 50
        if toDel != None:
            deleteSettings(toDel)
            del self.items[toDel]
    def offPress(self): pass
    def onScroll(self,di): pass
    def onKey(self,ev): pass
    def draw(self):
        pygame.draw.rect(screen,black,self.rect)
        pygame.draw.rect(screen,white,self.rect,2)
        x,y = tuple(self.rect[:2])
        for i in self.items:
            labelText = i[9:-4]
            simpleText(labelText,(x+4,y+1))
            for n in range(2):
                re = [x+4+n*170,y+25,20+40*(1-n),20]
                rCent = dA(re[:2],dD(re[2:],[2,2]))                
                pygame.draw.rect(screen,black,re)
                pygame.draw.rect(screen,white,re,2)
                centText(['Load','X'][n],rCent)
            y += 50
            pygame.draw.line(screen,white,(x,y),(x+self.rect[2],y),3)

class Presets:#Presets class, which allows the user to load a preset simulation
    mType = "M0"#defines the menu type as "M0", a menu class one below the menu buttons
    def __init__(self):#initialises the presets menu class
        self.rect = [ 250 , 60 , 200 , 630 ]
        self.visibile,self.subSelected = False, None
        self.items = ["Presets\\Life of a Fox.txt"]
    def onPress(self,mCo):#takes the mouse position, checks if the 'load' button was pressed for any preset
        x,y = tuple(self.rect[:2])
        toDel = None
        for c,i in enumerate(self.items):
            labelText = i[0:-4]
            simpleText(labelText,(x+4,y+1))
            re = [x+4,y+25,20+40,20]#'L'
            if inRect(mCo,re):
                runPreset()
            y += 50
    def offPress(self): pass#runs when menu is clicked off
    def onScroll(self,di): pass#runs when menu is scrolled on
    def onKey(self,ev): pass#runs when menu is typed on
    def draw(self):#draws the menu
        pygame.draw.rect(screen,black,self.rect)
        pygame.draw.rect(screen,white,self.rect,2)
        x = self.rect[0]
        y = self.rect[1]
        for i in self.items:
            labelText = i[8:-4]
            simpleText(labelText,(x+4,y+1))
            y += 25
            re = [x+4,y,60,20]
            rCent = dA(re[:2],dD(re[2:],[2,2]))                
            pygame.draw.rect(screen,black,re)
            pygame.draw.rect(screen,white,re,2)
            centText('Load',rCent)
            y += 25
            pygame.draw.line(screen,white,(x,y),(x+self.rect[2],y),3)
            
class DropDown:#A sub-menu class, which allows the user to select out of several options on a drop down meu
    mType = "M-1"#the menu type of "M-1" defines this menu as two below the main menu buttons
    def __init__(self,options,rect1,label='',sChoice=None):#initialises the dropdown menu class
        self.options,self.label,self.selOp = options, label, sChoice
        self.rect, self.rect1, self.rect2 = rect1[:], rect1[:], rect1[:]
        self.visibile = self.dropped = self.selected = False
        self.rect2[3] *= (len(options)+1)
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        if self.dropped:
            ind = (mCo[1]-self.rect2[1])//self.rect1[3] - 1
            if ind >= 0:
                self.selOp = self.options[ind]
                self.dropped = False
                self.rect = self.rect1[:]
            elif mCo[0]-self.rect1[0]-self.rect1[2]+20 > 0:
                self.dropped = False
                self.rect = self.rect1[:]
        elif mCo[0]-self.rect1[0]-self.rect1[2]+20 > 0:
            self.dropped = True
            self.rect = self.rect2[:]
    def offPress(self):
        mCo = pygame.mouse.get_pos()
        self.dropped = False
        self.rect = self.rect1[:]
        self.selected = False
    def onScroll(self,di): pass
    def onKey(self,ev): pass
    def draw(self):
        mCo = pygame.mouse.get_pos()
        simpleText(self.label,(self.rect[0]+2, self.rect[1]-20))
        pygame.draw.rect(screen,black,self.rect)
        pygame.draw.rect(screen,blue if self.selected else white,self.rect,2)
        x1 = self.rect[0]
        x2 = x1 + self.rect[2]
        simpleText(self.selOp if self.selOp != None else "No Selection",dA(self.rect[:2],[5,2]),white)
        mP = pygame.mouse.get_pos()
        dCol = white
        if mP[0]-self.rect1[0]-self.rect1[2]+20 > 0 and inRect(mP,self.rect1): dCol = [90]*3
        if self.dropped:
            iR = inRect(mP,self.rect)
            ind = (mCo[1]-self.rect2[1])//self.rect1[3] - 1
            for c,i in enumerate(self.options):
                y = self.rect[1]+self.rect1[3]*(c+1)
                if iR and c == ind: pygame.draw.rect(screen,[70]*3,[x1+2,y]+dS(self.rect1[2:],[4,0]))
                simpleText(i,(x1+5,y+2))
                pygame.draw.line(screen,blue,[x1,y],[x2,y],2)
            simpleText('▲',[x2-20,self.rect[1]],dCol)
        else:
            simpleText('▼',[x2-20,self.rect[1]],dCol)
    def output(self):
        return self.selOp
    def reset(self):
        self.selOp = None
#a shift conversion dictionary, stores a character and its' shift converted counterpart
sCD = {'/': '?', '-':'_', '\\':'|', "'": '"', '6': '^', '1': '!', '7': '&', '`': '~', '9': '(', '3': '#', '8': '*', ',': '<', '2': '@', '=': '+', '5': '%', ']': '}', ';': ':', '0': ')', '4': '$', '/': '?', '.': '>', '[': '{'}
def shiftConvert(key):#takes any character, and returns the shift converted version
    if key in sCD: return sCD[key]#if key is in the shift conversion key dictionary, convert it
    else: return key.upper()#otherwise, make the character uppercase
def indexTransfer(index,length):
    if index < 0: index += length
    elif index >= 0: index -= length
    return index
def indexInsert(st,ind,i):
    if ind == -1: return st + i
    else: return st[0:ind+1] + i + st[ind+1:]
    
class TextField:#A sub menu class, which allows the user to input text as input
    mType = "TF"#defines menu type of text field
    selected = False
    def __init__(self,rect,border=white,back=black,charLimit=30,charRange=range(32,127),label='',sText=''):#initialises the text field menu class
        self.rect,self.border,self.back,self.charLimit,self.charRange,self.label,self.sText = rect,border,back,charLimit, charRange, label, sText
        self.inText = sText
        self.cPos, self.ticks, self.delTick = -1, 0, None
        self.charLimit = self.rect[2]//myFontSize - 2
        self.numMode = (self.charRange == NUM_RANGE)
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        self.selected = True
    def offPress(self):
        self.selected = False
    def onKey(self,inEvent,linecap=100):
        keys = pygame.key.get_pressed()
        if self.selected:
            inString = self.inText
            sString = inString
            toAdd = ''
            if inEvent.type == pygame.KEYDOWN:
                toAdd = ''
                if self.charRange:
                    if inEvent.key in self.charRange: toAdd = chr(inEvent.key)
                else: toAdd = chr(inEvent.key)
                if inEvent.key == pygame.K_BACKSPACE:                 
                    if self.cPos == -1: inString = inString[:-1]
                    elif self.cPos != -len(self.inText)-1: inString = inString[:self.cPos] + inString[self.cPos+1:]
                elif inEvent.key == pygame.K_DELETE:                    
                    if self.cPos == -2: inString = inString[:-1]
                    elif self.cPos != -1: inString = inString[:self.cPos+1] + inString[self.cPos+2:]
                    self.cPos = min(self.cPos+1,-1)
                elif inEvent.key == pygame.K_LEFT:
                    tS = self.cPos
                    self.cPos = max(self.cPos-1,-len(self.inText)-1)
                elif inEvent.key == pygame.K_RIGHT:
                    tS = self.cPos
                    self.cPos = min(self.cPos+1,-1)
            if len(inString) < self.charLimit and toAdd != '':
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: toAdd = shiftConvert(toAdd)
                inString = indexInsert(inString,self.cPos,toAdd)
            self.inText = inString         
    def draw(self,add=(0,0)):
        extra = ''
        rect = self.rect[:]
        if self.back != None: pygame.draw.rect(screen,self.back,rect)
        pygame.draw.rect(screen,blue if self.selected else self.border,rect,2)
        simpleText(self.label,(rect[0]+2, rect[1]-20))
        t = simpleText(self.inText,(rect[0]+5,rect[1]+5))
        if self.selected and self.ticks%20 < 10: simpleText('_',(rect[0]+5+indexTransfer(self.cPos,len(self.inText))*12+12,rect[1]+5))
        if self.selected: self.ticks += 1
    def output(self):
        if self.numMode:
            if testValidFloat(self.inText): return float(self.inText)
            else: return None
        else:
            if self.inText == '': return None
            else: return self.inText
    def reset(self):
        self.inText = self.sText
        
class EventButton:#A sub menu class, which allows the user to press the button and run a given function
    mType = "EB"
    def __init__(self,rect,text='',ev=lambda : print("lmao") ):#initialises the event button class
        self.visibile = self.selected = False
        self.rect,self.text,self.ev = rect,text,ev
        self.center = dA(self.rect[:2],dD(self.rect[2:],[2]*2))
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        self.ev()
    def offPress(self): pass
    def onKey(self,ev): pass
    def onScroll(self,di): pass
    def draw(self):
        pygame.draw.rect(screen, [90]*3 if inRect(pygame.mouse.get_pos(),self.rect) else black,self.rect)
        pygame.draw.rect(screen,white,self.rect,2)
        centText(self.text,self.center)
    def reset(self):
        pass


class AddNewPlant:#A sub menu class, which allows the user to create a customised plant from given parameters
    mType="An"
    attributes = ["Species","Abundance","Lifespan","SaplingNum"]
    def __init__(self,parent,presets=None):#initialises the add new plant class
        self.rect = [500,60,200,390]
        if presets == None: sOps = [None,'1','1','1']
        else: sOps = presets
        self.subMenus = [
DropDown(["Grass","Tree"],dA(self.rect[:2],[10,30])+[180,30],"Species",sOps[0]),
TextField(dA(self.rect[:2],[10,190])+[180,30],charRange=NUM_RANGE,sText=sOps[1],label="Abundance"),
TextField(dA(self.rect[:2],[10,190+50])+[180,30],charRange=NUM_RANGE,sText=sOps[2],label="Lifespan"),
TextField(dA(self.rect[:2],[10,190+100])+[180,30],charRange=NUM_RANGE,sText=sOps[3],label="Sapling No."),
EventButton(dA(self.rect[:2],[10,190+150])+[180,40],"Add",self.output)
]
        self.pItemList = parent
        self.selected = False
        self.subSelected = None
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        for i in self.subMenus:
            if inRect(mCo,i.rect):
                if self.subSelected != None and i != self.subSelected:
                    self.subSelected.selected = False
                    self.subSelected.offPress()
                i.onPress(mCo)
                self.subSelected = i
                self.subSelected.selected= True
    def offPress(self):
        if self.subSelected != None: self.subSelected.selected = False
        self.subSelected = None
        for i in self.subMenus:
            i.reset()
        
    def onKey(self,ev):
        if self.subSelected != None: self.subSelected.onKey(ev)
    def onScroll(self,di): pass
    def draw(self):
        pygame.draw.rect(screen,black,self.rect)
        pygame.draw.rect(screen,white,self.rect,2)
        for i in self.subMenus:
            i.draw()
    def output(self):
        attributeDi = dict()
        invalid = False
        for c,i in enumerate(self.attributes):
            temp = self.subMenus[c].output()
            if temp == None:
                invalid = True
                break
            else:
                attributeDi[i] = temp
        if not invalid:
            self.pItemList.addItem(attributeDi)
            self.pItemList.parentMenu.listSelector()
            self.pItemList.parentMenu.selected = self.pItemList
            self.offPress()
            return attributeDi
            
        else:
            return None

class AddNewAnimal:#A sub menu class, which allows the user to create a customised animal from given parameters
    mType="An"
    attributes = ["Species","Diet","InitialPopulation","Lifespan","Hunger","Thirst","Clutch"]
    def __init__(self,parent,presets=None):#initialises the add new animal class
        self.rect = [500,60,200,630]
        if presets == None: sOps = [None,'Carnivore','1','1','1','1','1']
        else:
            sOps = presets
            sOps[1] = ["Herbivore","Carnivore"][int(sOps[1])]
        self.subMenus = [
DropDown(["Fox","Rabbit"],dA(self.rect[:2],[10,30])+[180,30],"Species",sOps[0]),
DropDown(["Herbivore","Carnivore"],dA(self.rect[:2],[10,190])+[180,30],"Diet",sOps[1]),
TextField(dA(self.rect[:2],[10,190+140])+[180,30],charRange=NUM_RANGE,sText=sOps[2],label="Inital Pop."),
TextField(dA(self.rect[:2],[10,190+190])+[180,30],charRange=NUM_RANGE,sText=sOps[3],label="Lifespan"),
TextField(dA(self.rect[:2],[10,190+240])+[180,30],charRange=NUM_RANGE,sText=sOps[4],label="Hunger"),
TextField(dA(self.rect[:2],[10,190+290])+[180,30],charRange=NUM_RANGE,sText=sOps[5],label="Thirst"),
TextField(dA(self.rect[:2],[10,190+340])+[180,30],charRange=NUM_RANGE,sText=sOps[6],label="Clutch"),
EventButton(dA(self.rect[:2],[10,190+390])+[180,40],"Add",self.output)
]
        self.pItemList = parent
        self.selected = False
        self.subSelected = None
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        for i in self.subMenus:
            if inRect(mCo,i.rect):
                if self.subSelected != None and i != self.subSelected:
                    self.subSelected.selected = False
                    self.subSelected.offPress()
                i.onPress(mCo)
                self.subSelected = i
                self.subSelected.selected= True
    def offPress(self):
        if self.subSelected != None: self.subSelected.selected = False
        self.subSelected = None
        for i in self.subMenus:
            i.reset()
        
    def onKey(self,ev):
        if self.subSelected != None: self.subSelected.onKey(ev)
    def onScroll(self,di): pass
    def draw(self):
        pygame.draw.rect(screen,black,self.rect)
        pygame.draw.rect(screen,white,self.rect,2)
        for i in self.subMenus:
            i.draw()
    def output(self):
        attributeDi = dict()
        invalid = False
        for c,i in enumerate(self.attributes):
            temp = self.subMenus[c].output()
            if temp == None:
                invalid = True
                break
            elif c == 1:
                attributeDi[i] = {"Herbivore":0,"Carnivore":1}[temp]
            else:
                attributeDi[i] = temp
        if not invalid:
            self.pItemList.addItem(attributeDi)
            self.pItemList.parentMenu.listSelector()
            self.pItemList.parentMenu.selected = self.pItemList
            self.offPress()
            return attributeDi
            
        else:
            return None
        
class ItemList:#A sub menu class, which stores lists of items, allowing creation of more as well as edits or deletion of existing items
    mType = "M-1"#the menu type of "M-1" defines this menu as two below the main menu buttons
    def __init__(self,rect,addNew=None,label='',parent=None,readAttri="Species"):#initialises the item list class
        self.rect1 = self.rect = rect
        self.visibile,self.selected,self.label,self.items,self.showLen,self.scroll,self.addNewType,self.addNewMenu,self.parentMenu,self.readAttri = True, False, label, [], 3, 0, addNew, addNew(self), parent, readAttri
        self.attributeList = addNew.attributes
        self.scrollRect = dA(rect[:2],[3+rect[2],0])+[5,rect[3]]
        self.drawLen = (rect[3])//(self.showLen + 1)
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        mCo = pygame.mouse.get_pos()
        if self.visibile:
            dIndex = (mCo[1]-self.rect[1])//self.drawLen
            sIndex = dIndex - 1 + self.scroll
            if dIndex == 0:
                self.addNewMenu = self.addNewType(self)                
                self.parentMenu.listSelector(self.addNewMenu)
            elif sIndex < len(self.items):
                xCo = (mCo[0]-self.rect[0])
                if 160 <= xCo <= 180:
                    del self.items[sIndex]
                elif 120 <= xCo < 140:
                    item = self.items[sIndex]
                    self.addNewMenu = self.addNewType(self,[str(item[a]) for a in self.attributeList])
                    del self.items[sIndex]    
                    self.parentMenu.listSelector(self.addNewMenu)
                maxScroll = max(0,len(self.items)-self.showLen)
                self.scroll = limit(self.scroll , maxScroll,0)
    def offPress(self):
        if not self.addNewMenu.selected:
            self.parentMenu.listSelector()
    def onScroll(self,di):
        maxScroll = max(0,len(self.items)-self.showLen)
        self.scroll = limit(self.scroll+di , maxScroll,0)     
    def onKey(self,ev): pass
    def draw(self):
        selCol = blue if self.selected else white
        pygame.draw.rect(screen,black,self.rect1)
        pygame.draw.rect(screen,selCol,self.rect1,2)
        simpleText(self.label,(self.rect1[0]+2, self.rect1[1]-20))
        simpleText("Add New +",dA(self.rect1[:2],[5,2]))
        pygame.draw.line(screen,selCol,dA(self.rect1[:2],[0,30]),dA(self.rect1[:2],[self.rect1[2],30]),2)
        for c,i in enumerate(self.items[self.scroll:self.scroll+self.showLen]):
            x = self.rect[0]
            y = self.rect[1] + self.drawLen*(c+1)
            pygame.draw.line(screen,blue if self.selected else white,[x,y+self.drawLen],[x+self.rect[2],y+self.drawLen],2)
            simpleText(i[self.readAttri],(x+5,y+2))
            simpleText("X",(x+self.rect[2]-18,y+2) )
            simpleText("E",(x+self.rect[2]-18-40,y+2) )
        pygame.draw.rect(screen,[140]*3,self.scrollRect)
        le = len(self.items)
        if le <= 3: scrollBarSize,scrollBarOff = 1,0
        else: scrollBarSize,scrollBarOff = 3/le,self.scroll/le
        h = self.scrollRect[3]+2
        pygame.draw.rect(screen,[140]*3,self.scrollRect)
        pygame.draw.rect(screen,white,dA(self.scrollRect[:2],[1,h*scrollBarOff]) + [self.scrollRect[2]-2 , h*scrollBarSize] )
    def addItem(self,nItem):
        self.items.append(nItem)
    def reset(self):
        self.items = []
    def output(self):
        return self.items

class Tutorial:#A menu class, displays text to the user describing how to play the game
    mType = "M0"#defines the menu type as "M0", a menu class one below the menu buttons
    title = "Tutorial"
    text = "This game simulates ecosystems; it simulates the interactions between animals and plants over time. You can customise your simulation in a variety of ways, or play a previous simulation. You can pause the game by changing the time multiplier to 0, you can view the analytics, or press on an animal to control it.\n \n If that doesn't take your fancy, you can play a preset simulation where you play as one animal and try to survive and beat quests. You will see the different actions as keys under different pictures. Arrow keys move your creature and WASD moves the camera if your perspective isn't locked."
    def __init__(self,rect=[ 250 , 60 , 545 , 630 ]):
        self.rect = rect
        self.visibile = self.selected = False
        self.lineLength = (self.rect[2]-5)//myFontSize
        self.rText = splitText(self.text,self.lineLength)
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        self.selected = True
    def offPress(self):
        self.selected = False
    def onKey(self,ev): pass
    def onScroll(self,di): pass
    def onKey(self,ev): pass
    def draw(self):
        if self.visibile:
            selCol = blue if self.selected else white
            pygame.draw.rect(screen,black,self.rect)
            pygame.draw.rect(screen,selCol,self.rect,2)
            lineText(self.rText,dA(self.rect,[5,30]))

class Credits:#A menu class, displays text to the user giving credits
    mType = "M0"#defines the menu type as "M0", a menu class one below the menu buttons
    title = "Credits"
    text = "This game was made by Samuel Price, but there are people I must thank. First of all I have to thank my teacher, Mr Thill.\n I also must credit the original artist for the pixel art I used that I did not make. The user Lampis on Pixalart designed the fox logo pixel art."
    def __init__(self,rect=[ 250 , 60 , 545 , 630 ]):#initialises the credits menu class
        self.rect = rect
        self.visibile = self.selected = False
        self.lineLength = (self.rect[2]-5)//myFontSize
        self.rText = splitText(self.text,self.lineLength)
    def onPress(self,mCo):#takes the menu position, and runs process for being clicked on
        self.selected = True
    def offPress(self):
        self.selected = False
    def onKey(self,ev): pass
    def onScroll(self,di): pass
    def onKey(self,ev):  pass
    def draw(self):
        if self.visibile:
            selCol = blue if self.selected else white
            pygame.draw.rect(screen,black,self.rect)
            pygame.draw.rect(screen,selCol,self.rect,2)
            lineText(self.rText,dA(self.rect,[5,30]))
    

#======================
#Main game loop
#======================

selected = None#initialises the selected variable to (None)
ticks = 0#initialises the ticks variable to 0
dTicks = 600#initialises day ticks at 600 (6:00am)

background = GradBackground((20,None,None) , (None,None,90) )#initialises the gradient background for a menu day night cycle

menuGUIs = [MenuButton("Past Trials",60,PastSims()),MenuButton("New Trial",120,NewTrial()),MenuButton("Presets",180,Presets()),MenuButton("Tutorial",240,Tutorial()),MenuButton("Credits",300,Credits())]#initialises the main menus with their y positions
menuGUIs += [i.subMenu for i in menuGUIs if i.subMenu != None]#adds each of the submenus of each main menu to the 'menuGUIs' array
while 1:#the loop always runs, and has no exit condition, since it is the mainline
    keys = pygame.key.get_pressed()#generates and stores an array of whether or not any given key is pressed
    mCo = pygame.mouse.get_pos()#generates and stores the mouse position
    for ev in pygame.event.get():#obtains the list of all queued events
        if ev.type == pygame.QUIT:#checks for the quit event
            pygame.quit(); quit()#quits pygame and python
        elif ev.type == pygame.MOUSEBUTTONDOWN:#checks for a mouse button clicked down event
            if ev.button == 1:#if the mouse button pressed was left click
                for i in menuGUIs:#looping through each menuGUI
                    if inRect(mCo,i.rect) and i.visibile:#if the mouse is inside the rectangle of the menu and the menu is visible
                        nSel = i.onPress(mCo)#sets the newly selected variable to be the output of the pressed menu's onPress function
                        if i.mType == "M1":#if the pressed menu was a main menu button
                            if selected != None: selected.offPress()#if there was a selected, press off
                            if selected == nSel: selected = None#if it is the same selected as previous, remove it from selection
                            else: selected = nSel#if it was different, set it as selected
                
            elif ev.button in [4,5]:#if the scroll wheel was used
                scrolled = False#initialises the scrolled variable as (False)
                for i in menuGUIs:#loops through the menu GUIs
                    if inRect(mCo,i.rect):#if the mouse in inside of this menu
                        scrolled = True#set the scrolled variable to be (True)
                        i.onScroll(ev.button*2-9)#runs the on scroll event, doing some math turning either button into a 0 or a 1
                        break#stops looking for more menus to scroll in
                    
        elif ev.type == pygame.KEYDOWN:#checks for key down event 
            if ev.key == pygame.K_F4 and keys[pygame.K_LALT]: pygame.quit(); quit()#if ALT and F4 are pressed, end the program
            if selected != None: selected.onKey(ev)#if a menu is selected, run the onKey event
                
    
    ##display
    background.update(dTicks)#updates the gradient (day-night cycle) background with the simulated day ticks
    pygame.draw.rect(screen,white,sRect,2)#draws a white border around the screen

    
    for i in menuGUIs:#looping through each menu GUI
        if i.visibile: i.draw()#if the menu is currently visible, draws it
    screen.blit(logo,logoPos)#blits the logo at the logo position on the right side of the screen

            
    PDU()#updates the display
    
    dTicks += 5#increments the day ticks variable by 5
    if dTicks >= DAY_DURATION:#if day ticks variable is greater than the duration of one day
        dTicks = dTicks - DAY_DURATION#sets 'dTicks' to the difference between 'dTicks' and 'DAY_DURATION'
    ticks += 1#increments the tick counter
    
    clock.tick(15)#runs the loop at 15 fps

    


