#this file defines functions which are called from the mainline, but need be in the mainline

import pygame
from math import sqrt,sin,cos,tan,atan,pi,e

#colour definitions
black = (0,0,0)
lightgray = (150,150,150)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkgray = (50,50,50)
brown = (101,67,33)
darkorange = (255,100,0)
darkgreen = (0,100,0)
darkred = (139,0,0)
yellow = (255,255,0)
darkyellow = (204,204,0)
grassGreen = (0,122,47)


#defines the four basic operations as a duple, addition, subtraction, multiplication, and division
def dA(d1,d2): return [d1[0]+d2[0],d1[1]+d2[1]]
def dS(d1,d2): return [d1[0]-d2[0],d1[1]-d2[1]]
def dM(d1,d2): return [d1[0]*d2[0],d1[1]*d2[1]]
def dD(d1,d2): return [d1[0]/d2[0],d1[1]/d2[1]]

def textObjects(text,font,colour=[255]*3):#renders text and returns the text surface and rectangle
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def resolve(r,theta): return r*sin(theta),r*cos(theta)#resolve a vector into its components

def magnitude(vec): return sqrt(vec[0]**2 + vec[1]**2)#determine magnitude of a vector

def inRect(co,rect): return rect[0] <= co[0] < rect[0]+rect[2] and rect[1] <= co[1] < rect[1]+rect[3]#return if a coordinate is inside a rect

def limit(n,t,b): return max(min(n,t),b)#limits the value of n between b and t

def coDistance(p0,p1): return magnitude(dS(p0,p1))#determines the distance between two coordinates

def findCorners(tL,le): return [tL,dA(tL,(le,0)),dA(tL,(le,le)),dA(tL,(0,le))]#finds the corners of a given square with side length le at position tL

def findRectCorners(rect): return [rect[:2] , dA(rect[:2],(rect[2],0)) , dA(rect[:2],rect[2:]) , dA(rect[:2],(0,rect[3])) ]#finds the corners of a rectangle

def sLFill(char,fill,le): return fill*max(0,le-len(char)) + char#fills in the space of a string with a given character to a given length

def unitVec(vec):#generates the unit vector a for a given vector
    mag = magnitude(vec)
    if mag == 0: return [0,0]
    else: return [i/mag for i in vec]

def ciS(m,arg): return [m*cos(arg) , m*sin(arg)]#returns the CiS expression given some argument 
def cMult(a,b,c,d): return [a*c - b*d, a*d + b*c]#does a complex multiplication operation given two complex numbers
def vecRot(co,d=1): return cMult(*ciS(1,d*2*pi)+co)#rotates a vector using complex number math

def minCorner(li,dim=3): return [min([i[d] for i in li]) for d in range(dim)]#returns the mininmum on each coordinate
def maxCorner(li,dim=3): return [max([i[d] for i in li]) for d in range(dim)]#returns the maxmimum on each coordinate
    
def nAdd(d1,d2): return [d1[n]+d2[n] for n in range(len(d1))]#adds two arrays of the same length [ d1[0] + d2[0] , d1[1] + d2[1], ... , d1[n] + d2[n] ]
def nSub(d1,d2): return [d1[n]-d2[n] for n in range(len(d1))]#subtracts two arrays of the same length [ d1[0] - d2[0] , d1[1] - d2[1], ... , d1[n] - d2[n] ]

def ciel(n): return -((-n)//1)#returns the integer next above or on a given decimal or integer
def satCalc(h): return h/(2*(h+1))#returns the amount of saturated hunger given (hunger above full)
def satICalc(s):return 2*s/(1-2*s)#inverse operation, returns the original amount of food taken to give a certain amount of saturation

def quad(oCo):#returns the quadrant of a certain coordinate, following trigonmetric rules 
    quad = 2; co = []
    for n in oCo:
        if n >= 0: co.append(1)
        else: co.append(-1)
    if sum(co) == 2: quad = 1
    elif sum(co) == -2: quad = 3
    elif co[0] > 0: quad = 4
    return quad

def twoCoAngle(co1,co2):#returns the bearing/angle between two points
    co2 = dS(co2,co1)
    co1 = [0,0]
    co2[1] *= -1
    
    if co2[0] != 0:
        qu = quad(co2)
        preAngle = atan(co2[1]/co2[0])*180/pi
        if qu == 1: angle = 90 - preAngle
        elif qu == 2:  angle = 270 - preAngle
        elif qu == 3: angle = 270 - preAngle
        elif qu == 4: angle = 90 - preAngle
    else:
        if co2[1] >= 0: angle = 0
        else: angle = 180
    return angle/360


def dF(li): return [int(i//1) for i in li]#returns the floored integers of every item in a given array

def stTime(t): return sLFill(str(t//100),'0',2)+':'+sLFill(str(int((t%100)*(60/100))),'0',2)#turns day ticks into a 24 hour time, with 100 ticks being 60 minutes

def aQCalc(a,L): return ((a/L)**10)*1000#returns the age quotient for a given age and lifespan

if __name__ == "__main__":#testing functions
    assert inRect([1,1],[0,0,2,2])
    assert not inRect([-1,-1],[0,0,2,2])
    assert dA([0,1],[2,3]) == [2,4]
    assert dM([0,1],[2,3]) == [0,3]
    assert dD([2,4],[1,2]) == [2,2]
    assert dS([1,2],[3,4]) == [-2,-2]
    print("TESTS PASSED")


