# Other modules
from time import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# My own modules
#from worldStatistic import WorldStatistic
from continent import Continent
from country import Country
from PIL.Image import *

# Global references to window and its properties
windowHandle = 0
initialWidth = 640
initialHeight = 480
initialXPosition = 0
initialYPosition = 0
fov = 45
programTitle = b"Worldly Globe"

# Controls
ESC = 27

# Data
years = ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004']
continentNames = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
allData = []
texturesTB = {}
texturesGDP = {}
texturesCO2 = {}
texturesPD = {}

# Selections within program
selectedTextures = 0
selectedYear = 0

#
# IMAGE AND TEXTURE GENERATION
#

#
# Generate a single texture ID and image pair
#
def getTextureImagePair(imageName):

    textureImage = Image()
    textureID = glGenTextures(1)
    try:
        imageFile = open(imageName)
        textureImage.sizeX = imageFile.size[0]
        textureImage.sizeY = imageFile.size[1]
        textureImage.data = imageFile.tobytes("raw", "RGBX", 0, -1)
    except:
        print("An image couldn't be loaded - program will exit.")
        sys.exit()
    
    return (textureID, textureImage)

def addToContinentData(continent, year, dataType, continentTexData):
    imageFilename = "maps/" + continent + dataType + year + ".bmp"
    textureData = getTextureImagePair(imageFilename)
    continentTexData[0][year] = textureData

#
# Load all necessary texture images.  
# Storage format: Key - continent name; Value: dictionary (key - year, 
# value - texture ID and image pair)
#
def loadTextureImages():
    global texturesTB, texturesGDP, texturesCO2, texturesPD

    for c in continentNames:
        continentTexDataTB = [{}]
        continentTexDataGDP = [{}]
        continentTexDataCO2 = [{}]
        continentTexDataPD = [{}]
        
        for y in years:
            addToContinentData(c, y, "TB", continentTexDataTB)
            addToContinentData(c, y, "GDP", continentTexDataGDP)
            addToContinentData(c, y, "CO2", continentTexDataCO2)
            addToContinentData(c, y, "PD", continentTexDataPD)
        texturesTB[c] = continentTexDataTB
        texturesGDP[c] = continentTexDataGDP
        texturesCO2[c] = continentTexDataCO2
        texturesPD[c] = continentTexDataPD

#
# Allows for easy obtaining of a particular texture ID and image
# based on a continent and a year, as a tuple.
# 0 - texture ID
# 1 - texture image
#
def getTextureImageDataPair(dataSource, continent, year):
    textureData = dataSource[continent]
    textureImagePair = textureData[0][year]
    
    return textureImagePair

#
# Handle the creation of textures from a particular dictionary
# of texture IDs and images based on a given statistical data type (TB, GDP,
# CO2, PD).
#
def initialiseTexturesFromSource(dataSource):
    
    for c in continentNames:
        for y in years:
            textureImagePair = getTextureImageDataPair(dataSource, c, y)
            textureID = textureImagePair[0]
            textureImage = textureImagePair[1]
            
            glBindTexture(GL_TEXTURE_2D, textureID)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, 4, textureImage.sizeX, 
                         textureImage.sizeY, 0, GL_RGBA, GL_UNSIGNED_BYTE, 
                         textureImage.data)

#
# Create textures from all texture data sources
#
def initialiseAllTextures():
    initialiseTexturesFromSource(texturesTB)      
    initialiseTexturesFromSource(texturesGDP)
    initialiseTexturesFromSource(texturesCO2)
    initialiseTexturesFromSource(texturesPD)    
#
# pyOpenGL SETUP
#
def startGL(width, height):

    """
        Initialise settings for background colour, depth testing, blending 
        and shading models.
    """
    # Load all textures
    print("Loading texture images...")
    loadTextureImages()
    initialiseAllTextures()
    print("Done.")
    
    glClearColor(0, 0, 0, 0)
    glClearDepth(1)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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
# DRAWING ABILITIES
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
    
    try:
        # Load all continent numerical data
        print("Loading data...")
        allData = Continent.generateFullContinentList()
        print("Done.")
        
        # Start up GLUT
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
    except Exception:
        print("Program couldn't start!")
        return 

main()
