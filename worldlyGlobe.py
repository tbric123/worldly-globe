# Other modules
from time import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# My own modules
#from worldStatistic import WorldStatistic
from continent import Continent
from country import Country

# Global references to window and its properties
windowHandle = 0
initialWidth = 640
initialHeight = 480
initialXPosition = 0
initialYPosition = 0
fov = 45
programTitle = b"Worldly Globe"

ESC = 27

# Data
years = ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004']
continentNames = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
allData = []

#
# pyOpenGL SETUP
#
def startGL(width, height):

    """
        Initialise settings for background colour, depth testing and shading
        models.
    """
    glClearColor(0, 0, 0, 0)
    glClearDepth(1)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    
    resizeWindow(width, height)

def resizeWindow(width, height):
    """
        Reconfigure drawing area (FOV, aspect ratio, near and far planes)
        and matrix type every time the window is resized.
    """
    if height == 0:
        height = 1
    
    glViewport(initialXPosition, initialYPosition, width, height)
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(fov, float(width)/float(height), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

#
# USER INPUT HANDLING
#
def keyPresses(key, x, y):
    """
        Handle all keyboard key presses.
    """
    key = ord(key)
    
    # Handle all keyboard controls
    if key == ESC:
        # ESC key - exit the program
        exitProgram()

def mouseClicks(button, state, x, y):
    """
        Handle all mouse clicks.
    """
    # Handle all mouse button clicks
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            exitProgram()

#
# DRAWING AND TEXTURING ABILITIES
#
def drawGlobe():
    """ 
        Main drawing function for the program. 
    """
    # Prepare to draw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-1, 0, -6)
    
    # Start drawing
    glColor3f(0, 0, 1)
    glutSolidSphere(1.5, 100, 100)
    
    # Make drawing appear on screen
    glutSwapBuffers()
    sleep(0.01)

#
# PROGRAM FEATURES
#    
def exitProgram():
    """ 
        Quick function call for exiting the program.
    """
    glutDestroyWindow(windowHandle)
    sys.exit()

#
# DATA INITIALISATION
#
def initialiseImages():
    pass

#
# PROGRAM STARTING POINT
# 
def main():
    global windowHandle
    global initialWidth
    global initialHeight
    global initialXPosition
    global initialYPosition
    global programTitle
    global allData
    
    # Start up GLUT
    try:
        print("Loading data...")
        allData = Continent.generateFullContinentList()
        print(allData)
        print("Done.")
        
        glutInit("")
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(initialWidth, initialHeight)
        glutInitWindowPosition(initialXPosition, initialYPosition)
        windowHandle = glutCreateWindow(programTitle)
        
        # Set up display, idle, resizing and keyboard handling functions
        glutDisplayFunc(drawGlobe)
        glutIdleFunc(drawGlobe)
        glutReshapeFunc(resizeWindow)
        glutKeyboardFunc(keyPresses)
        glutMouseFunc(mouseClicks)
        
        # Initialise OpenGL and run program 
        startGL(initialWidth, initialHeight)
        print("Opening window...")
        print("Worldly Globe - press ESC or right-click window to exit program.")  
        glutMainLoop()
    except:
        print("Program couldn't start:")
        return 

main()
