# Other modules
from time import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL.Image import *

# My own modules
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

# Scaling and rotating (tilting and panning)
scaleFactor = 0
tiltAmount = 0
panAmount = 0
TILT = 10
PAN = 10

# Limits enforced on zooming in and out
scalingUpperLimit = 4
scalingLowerLimit = -4
scale = 1

# Controls
ESC = 27

# Data
years = ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004']
continentNames = ["Europe", "Africa", "Asia", "North America", "Oceania", "South America"]
allData = []
texturesTB = {}
texturesGDP = {}
texturesCO2 = {}
texturesPD = {}

# Image file handling
BMP = ".bmp"
MAP_LOCATION = "maps/"

# Data Types
TB = "TB"
GDP = "GDP"
CO2 = "CO2"
PD = "PD"

# Default selections when program starts
defaultDataType = TB
defaultYearIndex = 0
defaultYear = years[defaultYearIndex]

# Selections within program
selectedDataType = defaultDataType
selectedYear = defaultYear
selectedYearIndex = defaultYearIndex
selectedContinentTextureIDs = [0, 0, 0, 0, 0, 0]

# Console Messages
IMAGE_NOT_FOUND = "An image couldn't be loaded - program will exit."
DATA_LOADING = "Loading data..."
TEXTURES_LOADING = "Loading textures..."
DONE = "Done."
EXITING = "Exiting..."
START_ERROR = "Program couldn't start."
WINDOW_OPEN = "Opening window..."
WELCOME = "Worldly Cube - press ESC or right-click window to exit program."
DISPLAY_TB = "Displaying average TB."
DISPLAY_GDP = "Displaying average GDP."
DISPLAY_CO2 = "Displaying average CO2."
DISPLAY_PD = "Displaying average PD."
YEAR_CHANGE = "Year changed to"
ZOOM_IN = "Zoomed in."
ZOOM_OUT = "Zoomed out."
ZOOM_IN_ATTEMPT = "Attempting to zoom in..."
ZOOM_OUT_ATTEMPT = "Attempting to zoom out..."
ZOOM_IN_LIMIT = "Can't zoom in any further!"
ZOOM_OUT_LIMIT = "Can't zoom out any further!"

#
# IMAGE AND TEXTURE GENERATION
#

def getTextureImagePair(imageName):
    """
        Generate a single texture ID and image pair.
    """
    textureImage = Image()
    textureID = glGenTextures(1)
    try:
        imageFile = open(imageName)
        textureImage.sizeX = imageFile.size[0]
        textureImage.sizeY = imageFile.size[1]
        textureImage.data = imageFile.tobytes("raw", "RGBX", 0, -1)
    except:
        print(IMAGE_NOT_FOUND)
        sys.exit()
    
    return (textureID, textureImage)

def addToContinentData(continent, year, dataType, continentTexData):
    """
        Helper method to assist in loading texture images by adding texture
        data to a given texture data storage area.
    """
    
    imageFilename = MAP_LOCATION + continent + dataType + year + BMP
    textureData = getTextureImagePair(imageFilename)
    continentTexData[0][year] = textureData

def loadTextureImages():
    """
       Load all necessary texture images.  
       Storage format: Key - continent name; Value: dictionary (key - year, 
       value - texture ID and image pair)
    """
    
    global texturesTB, texturesGDP, texturesCO2, texturesPD

    for c in continentNames:
        continentTexDataTB = [{}]
        continentTexDataGDP = [{}]
        continentTexDataCO2 = [{}]
        continentTexDataPD = [{}]
        
        for y in years:
            addToContinentData(c, y, TB, continentTexDataTB)
            addToContinentData(c, y, GDP, continentTexDataGDP)
            addToContinentData(c, y, CO2, continentTexDataCO2)
            addToContinentData(c, y, PD, continentTexDataPD)
        texturesTB[c] = continentTexDataTB
        texturesGDP[c] = continentTexDataGDP
        texturesCO2[c] = continentTexDataCO2
        texturesPD[c] = continentTexDataPD

def getTextureImageDataPair(dataSource, continent, year):
    """
       Allows for easy obtaining of a particular texture ID and image based on 
       a continent and a year, as a tuple.
       0 - texture ID
       1 - texture image
    """
    
    textureData = dataSource[continent]
    textureImagePair = textureData[0][year]
    
    return textureImagePair

def makeTextureSelection():
    """
        Make a selection of textures to display based on year and data type.
    """
    
    global selectedDataType, selectedYear, selectedContinentTextureIDs
    
    # Select texture data to access
    if selectedDataType == TB:
        dataSource = texturesTB
    elif selectedDataType == GDP:
        dataSource = texturesGDP
    elif selectedDataType == CO2:
        dataSource = texturesCO2
    else:
        dataSource = texturesPD
    
    # Set texture IDs for displaying textures on the cube
    i = 0
    for c in continentNames:
        textureData = getTextureImageDataPair(dataSource, c, selectedYear)
        textureID = textureData[0]
        selectedContinentTextureIDs[i] = textureID
        i += 1
    
def initialiseTexturesFromSource(dataSource):
    """
        Handle the creation of textures from a particular dictionary of 
        texture IDs and images based on a given statistical data type (TB, GDP,
        CO2, PD).
    """
    
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

def initialiseAllTextures():
    """
        Create textures from all texture data sources.
    """
    
    initialiseTexturesFromSource(texturesTB)      
    initialiseTexturesFromSource(texturesGDP)
    initialiseTexturesFromSource(texturesCO2)
    initialiseTexturesFromSource(texturesPD)    
    
    makeTextureSelection()

#
# pyOpenGL SETUP
#
def startGL(width, height):
    """
        Load continent data and textures and configure settings for 
        background colour, depth testing, blending and shading models.
    """
    
    # Load all numerical data for continents
    print(DATA_LOADING)
    allData = Continent.generateFullContinentList()
    print(DONE)
    
    # Load all textures
    print(TEXTURES_LOADING)
    loadTextureImages()
    initialiseAllTextures()
    print(DONE)
    
    # Display setting configuration
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
    
    global scaleFactor, scale, scalingUpperLimit, scalingLowerLimit
    global selectedDataType, selectedYear, selectedYearIndex
    key = ord(key)
    
    if key == ESC:
        # ESC key - exit the program
        exitProgram()
    elif key == ord('a') or key == ord('A'):
        # Display average TB on the cube
        print(DISPLAY_TB)
        selectedDataType = TB
        refreshDrawing()
    elif key == ord('s') or key == ord('S'):
        # Display average GDP on the cube
        print(DISPLAY_GDP)
        selectedDataType = GDP
        refreshDrawing()
    elif key == ord('d') or key == ord('D'):
        # Display average CO2 on the cube
        print(DISPLAY_CO2)
        selectedDataType = CO2
        refreshDrawing()
    elif key == ord('f') or key == ord('F'):
        # Display average PD on the cube
        print(DISPLAY_PD)
        selectedDataType = PD
        refreshDrawing()
    elif key == ord('w') or key == ord('W'):
        # Decrease year displayed by one year
        selectedYearIndex -= 1
        
        # Set minimum selection
        if selectedYearIndex < 0:
            selectedYearIndex = 0
        
        selectedYear = years[selectedYearIndex]
        print(YEAR_CHANGE, selectedYear)
        refreshDrawing()
    elif key == ord('e') or key == ord('E'):
        # Increase year displayed by one year
        selectedYearIndex += 1
        
        # Set maximum selction
        if selectedYearIndex >= len(years):
            selectedYearIndex = len(years) - 1  
                   
        selectedYear = years[selectedYearIndex]
        print(YEAR_CHANGE, selectedYear)
        refreshDrawing()
    elif key == ord('.') or key == ord('>'):
        # Zoom in
        scale += 1
        print(ZOOM_IN_ATTEMPT)
        if scale <= scalingUpperLimit:
            scaleFactor += 1
            print(ZOOM_IN)
        else:
            scale = scalingUpperLimit
            print(ZOOM_IN_LIMIT)
        refreshDisplay()
    elif key == ord(',') or key == ord('<'):
        # Zoom out
        scale -= 1
        print(ZOOM_OUT_ATTEMPT)
        if scale >= scalingLowerLimit:
            scaleFactor -= 1
            print(ZOOM_OUT)
        else:
            scale = scalingLowerLimit
            print(ZOOM_OUT_LIMIT)
        refreshDisplay()
        
def rotationControls(key, x, y):
    global tiltAmount, panAmount
    """
        Key handling function for rotating. A separate function is
        needed to read the arrow keys (or any other non-ASCII characters).
    """
    if key == GLUT_KEY_UP:
        # Tilt up by 10 degrees
        tiltAmount += TILT
        refreshDisplay()
    elif key == GLUT_KEY_DOWN:
        # Tilt down by 10 degrees
        tiltAmount -= TILT
        refreshDisplay()
    elif key == GLUT_KEY_LEFT:
        # Pan to right by 10 degrees
        panAmount += PAN
        refreshDisplay()
    elif key == GLUT_KEY_RIGHT:
        # Pan to left by 10 degrees
        panAmount -= PAN
        refreshDisplay()
        
def mouseClicks(button, state, x, y):
    """
        Handle all mouse clicks.
    """

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            print("Right mouse button clicked!")
    elif button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            print("Left mouse button clicked!")
            
#
# DRAWING ABILITIES
#

def drawCubeFace(size):
    """
        Draw a face for the world cube
    """
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0)
    glVertex3f(size, 0, 0)
    glTexCoord2f(1, 1)
    glVertex3f(size, size, 0)
    glTexCoord2f(0, 1)
    glVertex3f(0, size, 0)
    glEnd()
    
def drawWorldCube(textureIDs):
    """
        Draw the cube that will display continents.
    """
    
    size = 2
    glPushMatrix()
    
    faceIndex = 1
    for i in textureIDs:
        glBindTexture(GL_TEXTURE_2D, i)
        if faceIndex == 1:
            glTranslatef(-size/2, -size/2, -0.5)
        elif faceIndex == 2 or faceIndex == 3:
            glTranslatef(size, 0, 0)
            glRotatef(90, 0, 1, 0 )
        elif faceIndex == 4:
            glRotatef(-90, 1, 0, 0)
        elif faceIndex == 5:
            glRotatef(90, 1, 0, 0)
            glTranslatef(size, 0, 0)
            glRotatef(90, 0, 1, 0)
        else:
            glTranslatef( 0, size, 0 )
            glRotatef( -90, 1, 0, 0 )
        drawCubeFace(size)
        faceIndex += 1
        
    glPopMatrix()
    
def drawDisplay():
    """ 
        Main drawing function for the program. 
    """
    global scaleFactor
    
    # Prepare to draw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-1, 0, -6)
    glTranslate(0, 0, scaleFactor) # Zooming in and out
    glRotated(tiltAmount, 1, 0, 0) # Tilting
    glRotated(panAmount, 0, 1, 0) # Panning
    glEnable(GL_TEXTURE_2D)
    
    # Start drawing the cube
    glPushMatrix()
    drawWorldCube(selectedContinentTextureIDs)
    glPopMatrix()
    
    # Make drawing appear on screen
    glutSwapBuffers()

#
# PROGRAM FEATURES
#    
def exitProgram():
    """ 
        Quick function call for exiting the program.
    """
    print(EXITING)
    glutDestroyWindow(windowHandle)
    sys.exit()

def refreshDrawing():
    """
        Update textures and drawings.
    """
    makeTextureSelection()
    drawDisplay()
    
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
    
    try: 
        # Start up GLUT
        glutInit("")
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(initialWidth, initialHeight)
        glutInitWindowPosition(initialXPosition, initialYPosition)
        windowHandle = glutCreateWindow(programTitle)
    
        # Set up display, idle, resizing and mouse and keyboard handling functions
        glutDisplayFunc(drawDisplay)
        glutIdleFunc(drawDisplay)
        glutReshapeFunc(resizeWindow)
        glutKeyboardFunc(keyPresses)
        glutMouseFunc(mouseClicks)
        glutSpecialFunc(rotationControls) # For non-ASCII keys (i.e. arrow keys)
    except:
        print(START_ERROR)
        return 
    
    # Initialise OpenGL and run program 
    startGL(initialWidth, initialHeight)
    print(WINDOW_OPEN)
    print(WELCOME)
    glutMainLoop()
    
main()