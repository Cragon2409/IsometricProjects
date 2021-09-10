

###importing libraries
import pygame
from random import randrange,seed
from math import sqrt,sin,pi,cos,tan,atan,e
#1
seed(1)

###pygame initialisation and setup
##dh = dw = 840#defines the display width and height to be 840

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
dw,dh = tuple(screen.get_size())
##dh -= 70
screen = pygame.display.set_mode((dw,dh))
##print(dw,dh)
sCent = [dw/2,dh/2]
sRect = [0,0,dw,dh]
sRect = [0,0,dw-2,dh-2]
clock = pygame.time.Clock()

pygame.font.init()
myFont = pygame.font.SysFont("monospace", 20)
myFont2 = pygame.font.SysFont("monospace", 15)
fancyFont = pygame.font.SysFont("calibri", 22)
bigfont = pygame.font.SysFont("calibri", 50)

capText = "Testing"
pygame.display.set_caption(capText)

##pygame.mouse.set_visible(False)

black = (0,0,0)

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
orange = (255,128,0)
yellow = (237,212,62)

    

###General operations functions definitions
def dupleAdd(d1,d2): return [d1[0]+d2[0],d1[1]+d2[1]]
def dupleMin(d1,d2): return [d1[0]-d2[0],d1[1]-d2[1]]
def dupleMult(d1,d2): return [d1[0]*d2[0],d1[1]*d2[1]]
def dupleDivide(d1,d2): return [d1[0]/d2[0],d1[1]/d2[1]]

def textObjects(text,font,colour=white):#does text rendering
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def simpleText(inputText,co=(0,0),colour=white,font = myFont):#draws text to the screen
    text = font.render(inputText, True, colour)
    screen.blit(text,co)
def centText(inputText,center,colour=white,font=myFont):
    textSurf, textRect = textObjects(inputText,font,colour)
    textRect.center = center
    screen.blit(textSurf,textRect)
    
def messageDisplay(text,colour=white,size=50,center = [dw/2,dh/2] ,font = 'Calibri'):#draws a centered text in the middle of the screen
    largeText = pygame.font.SysFont(font,size)
    TextSurf, TextRect = textObjects(text,largeText,colour)
    TextRect.center = center
    screen.blit(TextSurf, TextRect)

def resolve(r,theta): return r*sin(theta),r*cos(theta)#resolve a vector into its components

def magnitude(vec): return sqrt(vec[0]**2 + vec[1]**2)#determine magnitude of a vector

def inRect(co,rect): return rect[0] <= co[0] < rect[0]+rect[2] and rect[1] <= co[1] < rect[1]+rect[3]#return if a coordinate is inside a rect

def limit(n,t,b): return max(min(n,t),b)#limits the value of n between b and t

def coDistance(p0,p1): return magnitude(dupleMin(p0,p1))#determines the distance between two coordinates

def findCorners(tL,le): return [tL,dupleAdd(tL,(le,0)),dupleAdd(tL,(le,le)),dupleAdd(tL,(0,le))]#finds the corners of a given square with side length le at position tL

def findRectCorners(rect): return [rect[:2] , dupleAdd(rect[:2],(rect[2],0)) , dupleAdd(rect[:2],rect[2:]) , dupleAdd(rect[:2],(0,rect[3])) ]#finds the corners of a rectangle

def rToD(co): return [ zoom*(st1*co[0]+ct1*co[1]) + add[0] , zoom*C*(ct1*co[0]-st1*co[1]) + co[2]*V*zoom + add[1] ]#turns real coordinates into draw coordinates

def dToR(co,z=0):#turns drawing coordinates into real coordinates (given z)
    yR = st1 * ( (co[1]-add[1]-V*z*zoom) / (-zoom*C) + ct1*((co[0]-add[0])/(zoom*st1)))
    xR = (co[0]-add[0]-zoom*ct1*yR) / (zoom*st1)
    return [xR,yR]

def distCalc(d): return zoom*d*sqrt((1-C)*(sin(2*theta)-1)+2)

PDU = pygame.display.update# shortens typing

def setView(rCo,dCo=[dw//2,dh//2]): return [ dCo[0]-zoom*(sin(theta)*rCo[0]+cos(theta)*rCo[1]) , dCo[1]-zoom*C*(cos(theta)*rCo[0]-sin(theta)*rCo[1])-zoom*V*rCo[2] ]#returns the needed camera offset to make a certain real coordinate appear at a given screen coordinate.


#Top,Bottom,Left,Front,Right,Back
def drawRectPrism(rectPrism,colours,outline=None):#draws a rectangular prism of [x,y,z,width,height,length] of given colour, and returns wether or not it was drawn on the screen.
    li = [rToD(co+[rectPrism[2]]) for co in findRectCorners(rectPrism[:2] + rectPrism[3:5])]
    
    li2 = [rToD(co+[rectPrism[2]+rectPrism[5]]) for co in findRectCorners(rectPrism[:2] + rectPrism[3:5])]
    
    tModeA = (t%180)//90
    tModeB = t//180
    tModeC = t//90

##    colours = [[60,90,200]]*2 + [[55,95,210],[50,90,215],[55,85,220],[50,90,210]]
    colours = [colours]*6
    dTheta = theta*(180/pi)
    dModeC = int(dTheta//90)
    
    if tModeC in [2,1]:
        if colours[1] != None:
            pygame.draw.polygon(screen,colours[1],li2)
            if outline != None: pygame.draw.polygon(screen,outline,li2,2)
    else:
        if colours[0] != None:
            pygame.draw.polygon(screen,colours[0],li)
            if outline != None: pygame.draw.polygon(screen,outline,li,2)
    
    for n in  [[3,2,1,0],[0,1,2,3]][tModeB] :
        n = (n-dModeC)%4
        if colours[n+2] != None:
            pygame.draw.polygon(screen,colours[n+2] ,[li[n],li2[n],li2[(n+1)%4],li[(n+1)%4]])
            if outline != None: pygame.draw.polygon(screen,outline ,[li[n],li2[n],li2[(n+1)%4],li[(n+1)%4]],2)
        
    if tModeC in [0,3]:
        if colours[0] != None:
            pygame.draw.polygon(screen,colours[0],li)
            if outline != None: pygame.draw.polygon(screen,outline,li,2)
    else:
        if colours[1] != None:
            pygame.draw.polygon(screen,colours[1],li2)
            if outline != None: pygame.draw.polygon(screen,outline,li2,2)




            
#=============================
###Modelling Classes & Functions
#=============================#


def topLeft(li,dims=3):
    return [ min([i[n] for i in li]) for n in range(dims) ]
def depthIndex(N):
    return (V)*((N[0])*ct1-(N[1])*st1)-(C)*(N[2])

dimDi = {'x':0,'y':1,'z':2}
def cr(v1,v2,dims):
    dims = [dimDi[i] for i in dims]
    return v1[dims[0]]*v2[dims[1]] - v1[dims[1]]*v2[dims[0]]

def showModel():#uses objects list
    tObjects = sorted(triangles,key=lambda x:depthIndex(topLeft([points[c] for c in x])) )# + C*(x.dim[0]*st1-x.dim[1]*ct1) + V*(x.dim[2])   )#less again

    
    for tri in tObjects:
##        col = [limit([30,80,210][c]+i/2,255,0) for c,i in enumerate(colour(coDistance(points[tri[0]],(0,0))))]
        col = colour(sum([points[tri[n]][2] for n in range(3)]))        
        poly = [rToD(points[i]) for i in tri]
        pygame.draw.polygon(screen,col,poly)
        pygame.draw.polygon(screen,[i*0.8 for i in col],poly,1)


#assumes all are same dim

#=============================
###RunTime
#=============================

##rotDi = {pygame.K_a:-1,pygame.K_d:1}#stores the keys and proportions for turning the car
zDi =  {5:0.9 , 4:1.11}#stores the mouse button (scroll wheel) and realted numbers for zooming in and out
temp = {pygame.K_UP:-1,pygame.K_DOWN:1}#stores the keys and proportions for shifting the camera down and up
addDi = {pygame.K_w:(0,1),pygame.K_a:(1,0),pygame.K_s:(0,-1),pygame.K_d:(-1,0)}


showFPS = True#whether or not to show fps on the screen


C1 = [1.08,2.68,6.76]
N1 = [3.28,0.32,2.2]
FR = 0.1#0.052
def colour(num):
    num -= 1
    fr = FR
    r = round(sin(fr*num*N1[0]+C1[0])*127+128)
    g = round(sin(fr*num*N1[1]+C1[1])*127+128)
    b = round(sin(fr*num*N1[2]+C1[2])*127+128)
    return r,g,b

zoom = 28#107.15#70.74
t = 71
C = cos((pi/180)*t)
theta = 4*pi/3 + 0.01
V = sin((pi/180)*t)

gameExit = False#game exit flag
ticks = 0


##Poly Setup
##cubeRectP = [0]*3+[3]*3
ROW = 100
points = [ [(n%ROW),(n//ROW),randrange(-50,51)/100] for n in range(ROW**2) ]
for i in points:
    i[0] += randrange(-30,31)/100
    i[1] += randrange(-30,31)/100
    
pointsB= points[:]
pointsVel = [ [randrange(-50,51)/500 for n in range(3)] for i in points]
triangles = [ [n,n+1,n+ROW] for n in range(ROW**2-ROW) if n%ROW != ROW-1 ]
triangles +=[ [n+1,n+ROW,n+ROW+1] for n in range(ROW**2-ROW) if n%ROW != ROW-1 ]

rainDrops = [ [randrange(0,ROW*100)/100 for n1 in range(2)] + [-10] + [randrange(80,100)/10] for n in range(0) ]

#ripples = [ [origin,distance,speed,amplitude,period] , ... ]
ripples = [ [[randrange(0,ROW*100)/100 for n1 in range(2)],randrange(-10,100)/40,0.3*20,randrange(20)/20,randrange(5,100)/50] for n in range(4) ]


def hf(x,period=2): return x  #return sin(x**2)/(x**2)


peak = 5
##def formula(x):
####    return math.cos(num**1.12/4+num**1.05/6+math.sin(x))*heightAccent
##    x/= 1000
####    print(x)
##    try: return peak/2*cos((x**1.12)/3 + sin(x + sin(-4.9*x)) + atan(x)*3 ) + peak//2
##    except:
##        print(x)
##        x = round(x,5)
##        print(x)
##        return peak/2*cos((x**1.12)/3 + sin(x + sin(-4.9*x)) + atan(x)*3 ) + peak//2
N3 = 2.2
##fInfo = [(-0.67,2.8),(2.6,2.8),(3.66,5.26),(2.4,-5.2),(3,3.16)]
##fInfo = [(-0.12,0.63),(0.43,2.8),(1.21,5.26),(0.98,-5.2),(2.1,3.16),(0.97,2),(3.87,4),(-4.93,-6.29),(1.11,-0.79),(-4.33,-9.13),(-9.25,3.93),(-6.91,5.05),(-2.57,-6.87),(9.53,-8.43),(-6.77,7.59),(6.81,-0.03),(7.01,-8.09)]
fInfo = [(-0.12,0.93),(0.43,2.8),(1.21,5.26),(0.98,-5.2),(2.1,3.16),(0.97,2),(3.87,4),(-4.93,-6.29),(1.11,-0.79),(-4.33,-9.13),(-9.25,3.93),(-6.91,5.05),(-2.57,-6.87),(9.53,-8.43),(-6.77,7.59),(6.81,-0.03),(7.01,-8.09)]

fInfo2 = [(-0.22,0.68),(0.61,2.8),(2.21,5.26),(0.48,-5.2),(3.1,3.16),(2.97,2),(4.81,2.8),(-1.35,-0.53),(4.73,-7.07),(5.95,-4.65),(-3.23,6.75),(5.87,7.01),(4.89,6.89),(1.87,-8.89),(4.79,-8.99),(-7.05,9.49),(-6.29,3.99)]
mZoom = 5#2
##def formula(x):
##    return sum([ N3**(-c))*cos(i[0]*x+i[1]) for c,i in enumerate(fInfo) ])
##    return sum([ N3**(-(c//2))*cos(i[0]*x+i[1]) for c,i in enumerate(fInfo) ])
##def formula2(x):
##    return sum([ N3**(-(c//2))*sin(i[0]*x+i[1]) for c,i in enumerate(fInfo2) ])
def formula3(x,y):
    x /= mZoom; y /= mZoom
    return sum([ N3**(-(c//2))*cos(i[0]*x+i[1])*sin(fInfo2[c][0]*y+fInfo2[c][1]) for c,i in enumerate(fInfo) ])

def g(x): return -2.6**(-x*0.9)-0.2

for c,i in enumerate(points):
    tX,tY = tuple(i[:2])
    
    hAdd = 2*g(formula3(tX,tY))#formula(tY-tX/10)*formula2(tX+tY/10) #sum([hf(coDistance(ripple[0],i)-ripple[1],ripple[4])*ripple[3] for ripple in ripples])
    points[c] = [pointsB[c][0],pointsB[c][1],hAdd+2*sin(ticks/20-pointsB[c][2])/(10+pointsB[c][2])]

block = None#[pos,dim,vel]

while not gameExit:
    ##event handler
    keys = pygame.key.get_pressed()#gets pressed keys
    mCo = pygame.mouse.get_pos()#gets mouse positition
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: pygame.quit(); quit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button in [4,5]:                    
                for b in zDi:
                    if ev.button == b: zoom *= zDi[b]#changes the zoom level
##            elif ev.button == 1:
##                pS = [dToR(mCo,z)+[z] for z in range(4)]
##                mRCo = dToR(mCo,0)
##                ripples.append([mRCo,0,0.3,0.2,5])
##        elif ev.type == pygame.MOUSEBUTTONUP:
##            if ev.button == 1: selected = None
            
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_F4 and keys[pygame.K_LALT]: pygame.quit(); quit()
        


    ##checks for keys pressed to move camera
    for k in temp:#changes vertical camera angle
        if keys[k]:
            t = (t+5*temp[k])%360
            C = cos(t*(pi/180))#sets C
            V = sin(t*(pi/180))#sets V
            drawAxis = True
            
    theta += (pi/180)
    st1 = sin(theta)
    ct1 = cos(theta)
    drawAxis = True

    add = setView([ROW/2]*2+[0],sCent)

##    if not ticks%2:
##        for c,i in enumerate(points):
##            tX,tY = tuple(i[:2])
##            
##            hAdd = g(formula3(tX+ticks/2,tY))#formula(tY-tX/10)*formula2(tX+tY/10) #sum([hf(coDistance(ripple[0],i)-ripple[1],ripple[4])*ripple[3] for ripple in ripples])
##            points[c] = [pointsB[c][0],pointsB[c][1],hAdd+2*sin(ticks/20-pointsB[c][2])/(10+pointsB[c][2])]
    
    ##display
    screen.fill(black)#[50-50*cos((ticks/101)),50+50*cos(ticks/863),50+50*sin(ticks/207+2)])#background colour changes over time
    pygame.draw.rect(screen,white,sRect,2)
    
    p = showModel()
    
##    if block != None: drawRectPrism(block[0]+block[1],[120,130,100])
    
##    for rainDrop in rainDrops:
##        rainDrop2 = rainDrop[:]
##        dI = abs(depthIndex(rainDrop[:3])) + 0.1
##        col = [limit([10,20,110][c]+i/20,255,0) for c,i in enumerate(colour(coDistance(rainDrop,[ROW]*2)))]
##        drawRectPrism(rainDrop[:3]+[0.02,0.02,0.3],[10,20,210])
    
    simpleText(str(t))
    simpleText(str(int((theta*(180/pi))%360)),(0,30))
    if showFPS: simpleText(str(round(clock.get_fps(),2))+" fps",(dw-100,30))#shows FPS if turned on




##    
####    toDel = []
####    for c,i in enumerate(ripples):
####        i[1] += i[2]
####        i[3] *= 0.99
####        if i[1] > sqrt(2)*ROW or abs(i[3]) < 0.01: toDel.append(c)
####    for c in toDel[::-1]:
####        del ripples[c]
####        ripplesN = 0
####        if randrange(1,3) == 1: ripplesN += 1
####        for n in range(ripplesN):ripples.append([[randrange(0,ROW*100)/100 for n1 in range(2)],0,0.3*20,0.2,5])


    


    PDU()#updates the display

    
    
    clock.tick(30)#30 fps 
    ticks += 1#tick increment



