import pygame as p
import math as m
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

screenWidth = 800
screenHeight = 600

arm_1 = 100
arm_2 = 100
maxSpeed = 3

class robotMe:
    def __init__(self, x0, y0, myHeading, myColor):
        self.x = x0
        self.y = y0
        self.wayX = 0
        self.wayY = 0
        self.heading = myHeading
        self.color = myColor
        self.vel = 0
        self.hitRad = 10

    def drawMe_ForwardKinematics(self, w, deg_1, deg_2):
        headingInRadians = deg2Rad(deg_1)
        px_1 = self.x + arm_1*m.cos(headingInRadians)
        py_1 = self.y + arm_1*m.sin(headingInRadians)

        w.line(self.x, self.y, px_1, py_1, RED, 5)

        headingInRadians = deg2Rad(deg_1 + deg_2)
        px_2 = px_1 + arm_2*m.cos(headingInRadians)
        py_2 = py_1 + arm_2*m.sin(headingInRadians)

        w.line(px_1, py_1, px_2, py_2, RED, 5)
        return
    
    def InverseKinematics(self, w, px3, py3):
        
        px3, py3 = orientXY(px3, py3)

        a = arm_2
        b = arm_1

        px1 = self.x
        py1 = self.y

        D = m.atan2(py3-py1, px3-px1)

        c = m.sqrt((px3-px1)**2 + (py3-py1)**2)

        forA = (b**2 + c**2 - a**2)/(2*b*c)

        #set forA to meet the domain of acos if too large
        if forA <= -1:
            forA = -.9999999
        elif forA >= 1:
            forA = .9999999
        
        A = m.acos(forA)

        C = m.asin(deg2Rad(m.sin(A)*c/a))

        px2 = px1 + arm_1*m.cos(A+D)
        py2 = py1 + arm_1*m.sin(A+D)

        w.line(px1, py1, px2, py2, YELLOW, 5)
        w.line(px2, py2, px3, py3, YELLOW, 5)
        
        return

#class to draw lines
class window:
    def __init__(self, surf, xmin, ymin, xmax, ymax):
        self.mySurface = surf
        self.xMin = xmin
        self.yMax = ymin
        self.xMax = xmax
        self.yMax = ymax
        return
    
    def line(self, x0, y0, x1, y1, color, width):
        xs, ys = orientXY(x0, y0)
        xe, ye = orientXY(x1, y1)
        p.draw.line(self.mySurface, color, [xs, ys], [xe, ye], width)
        return
        
def orientXY(x0, y0):
    x = int(x0)
    y = int(screenHeight - y0)
    return x, y

def deg2Rad(deg):
    rad = deg/180.0 * m.pi
    return rad

def rad2Deg(rad):
    deg = rad/m.pi * 180.0
    return deg

def dist(x0, y0, x1, y1):
    myDist = (x1 - x0)*(x1 - x0) + (y1 - y0)*(y1 - y0)
    myDist = m.sqrt(myDist)
    return myDist


def runGame():
    # Initialize pygame
    p.init()
    
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)
    
    # Initialize window.
    w = window(screen, 0, screenWidth, 0, screenHeight)
    
    # Create the window caption
    p.display.set_caption("2 DOF Robot Arm")
     
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
    
    # Create a robot.
    r = robotMe(400, 300, 90, CYAN)

    d1 = 90
    d2 = 90

    px3 = 300
    py3 = 400
    
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        #print(p.mouse.get_pos())
        px3, py3 = p.mouse.get_pos() #gets mouse location on screen
        

        w.line(50, 50, 50, 50, RED, 20)

        
        screen.fill(BLACK) #used to erase prior data on screen so it doesn't duplicate

        
        r.drawMe_ForwardKinematics(w, d1, d2)

        r.InverseKinematics(w, px3, py3)
        
       
        p.display.flip()#updates the screen
        
        clock.tick(20)#limits to 20fps
    
    # Close the window and quit.
    p.quit()
    
    return

runGame()
