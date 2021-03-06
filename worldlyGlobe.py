# Other modules
from time import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL.Image import *
from math import *

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
years = ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', 
         '2005', '2004']
continentNames = ["Europe", "Africa", "Asia", "North America", "Oceania", 
                  "South America"]
rotationalPositions = {"Europe":(0, 0), "Africa":(0, -90), "Asia":(0, 180), 
                       "North America":(-90, 0), "Oceania":(0, 90), 
                       "South America":(90, 90)}
locationPositions = {(0, 0):"Europe", (180, 180):"Europe", (-180, -180):"Europe",
                     (-180, 180):"Europe", (180, -180):"Europe", (0, -90):"Africa", 
                     (180, 90):"Africa", (-180, 90):"Africa", (0, 180):"Asia", 
                     (180, 0):"Asia", (0, -180):"Asia", (-180, 0):"Asia", 
                     (-90, 0):"North America", (-90, -90):"North America", 
                     (-90, -180):"North America", (-90, 180):"North America",
                     (-90, 90):"North America", (0, 90):"Oceania", (-180, 90):"Oceania", 
                     (180, -90):"Oceania", (-180, -90):"Oceania", 
                     (90, 90):"South America", (90, 0):"South America", 
                     (90, -90):"South America", (90, 180):"South America", 
                     (90, -180):"South America"}
allData = []
texturesTB = {}
texturesGDP = {}
texturesCO2 = {}
texturesPD = {}
currentValue = 0
currentGradient = 0
currentIntercept = 0

# Image file handling
BMP = ".bmp"
MAP_LOCATION = "maps/"

# Data Types
TB = "TB"
GDP = "GDP"
CO2 = "CO2"
PD = "PD"
dataTypes = {TB:1, GDP:2, CO2:3, PD:4}
units = {TB:"deaths/capita", GDP:"$US/capita", CO2:"tonnes/capita", 
         PD:"people/km^2"}

# Default selections when program starts
defaultDataType = TB
defaultYearIndex = 0
defaultYear = years[defaultYearIndex]
defaultContinent = "Europe"

# Selections within program
selectedDataType = defaultDataType
selectedYear = defaultYear
selectedYearIndex = defaultYearIndex
selectedContinentTextureIDs = [0, 0, 0, 0, 0, 0]
selectedContinent = defaultContinent

# Text positioning on-screen
xTextPos = 3
yTextPosDT = -2
yTextPosY = yTextPosDT - 0.08
yTextPosV = yTextPosY - 0.08
yTextPosC = yTextPosDT + 0.08

# Colour bar settings
bottomInterval = 0
topInterval = 2
currentArrowPosition = 0

# Lighting
lightRange = 2
lightTheta = 0
lightPhi = 45

# Console Messages
IMAGE_NOT_FOUND = "An image couldn't be loaded - program will exit."
DATA_LOADING = "Loading data..."
TEXTURES_LOADING = "Loading textures..."
DONE = "Done."
EXITING = "Exiting..."
START_ERROR = "Program couldn't start."
WINDOW_OPEN = "Opening window..."
WELCOME = "Worldly Cube - press ESC or right-click window to exit program."
DISPLAY_TB = "Displaying median TB."
DISPLAY_GDP = "Displaying median GDP."
DISPLAY_CO2 = "Displaying median CO2."
DISPLAY_PD = "Displaying median PD."
YEAR_CHANGE = "Year changed to"
ZOOM_IN = "Zoomed in."
ZOOM_OUT = "Zoomed out."
ZOOM_IN_ATTEMPT = "Attempting to zoom in..."
ZOOM_OUT_ATTEMPT = "Attempting to zoom out..."
ZOOM_IN_LIMIT = "Can't zoom in any further!"
ZOOM_OUT_LIMIT = "Can't zoom out any further!"

# Right click menu resources
def selectAfrica():
    global selectedContinent
    selectedContinent = "Africa"
    fixateOnContinent(selectedContinent)

def selectAsia():
    global selectedContinent
    selectedContinent = "Asia"
    fixateOnContinent(selectedContinent)

def selectEurope():
    global selectedContinent
    selectedContinent = "Europe"
    fixateOnContinent(selectedContinent)

def selectNorthAmerica():
    global selectedContinent
    selectedContinent = "North America"
    fixateOnContinent(selectedContinent)

def selectOceania():
    global selectedContinent
    selectedContinent = "Oceania"
    fixateOnContinent(selectedContinent)

def selectSouthAmerica():
    global selectedContinent
    selectedContinent = "South America"
    fixateOnContinent(selectedContinent)
    
def continentMenu(item):
    options[item]()
    return 0

africaItem, asiaItem, europeItem, naItem, oceaniaItem, saItem = list(range(6))
options = {africaItem:selectAfrica, asiaItem:selectAsia, 
           europeItem:selectEurope, naItem:selectNorthAmerica,
           oceaniaItem:selectOceania, saItem:selectSouthAmerica}

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

def setCurrentValue():
    """
        Sets the current value based on the selected data
        type, year and continent.
    """
    global currentValue, allData, selectedContinent
    for c in allData:
        if c.getName() == selectedContinent:
            currentValue = c.getMedianValue(selectedYear, dataTypes[selectedDataType])
            return

def setDisplayedContinentText():
    """
        Sets the name of the continent that will be displayed on-screen.
    """
    global selectedContinent, locationPositions
    try:
        selectedContinent = locationPositions[(tiltAmount, panAmount)]
    except:
        return

def setArrowPosition():
    """
        Sets the position of the arrow on the colour bar based on the current 
        value.
    """
    global currentValue, currentArrowPosition, selectedContinent
    global currentIntercept, currentGradient
    for c in allData:
        if c.getName() == selectedContinent:
            
            currentGradient, currentIntercept = c.calculateGradientAndIntercept(
                    dataTypes[selectedDataType], bottomInterval, topInterval)           
            currentArrowPosition = currentValue * currentGradient + currentIntercept
            return
    
#
# pyOpenGL SETUP
#
def startGL(width, height):
    """
        Load continent data and textures and configure settings for 
        background colour, depth testing, blending and shading models.
    """
    global allData, locationPositions
    
    # Load all numerical data for continents
    print(DATA_LOADING)
    allData = Continent.generateFullContinentList()
    print(DONE)
    
    # Load all textures
    print(TEXTURES_LOADING)
    loadTextureImages()
    initialiseAllTextures()
    print(DONE)
    
    setCurrentValue()
    setArrowPosition()
    setDisplayedContinentText()
    
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
        # Display median TB on the cube
        selectedDataType = TB
        refreshDisplay()
    elif key == ord('s') or key == ord('S'):
        # Display median GDP on the cube
        selectedDataType = GDP
        refreshDisplay()
    elif key == ord('d') or key == ord('D'):
        # Display median CO2 on the cube
        selectedDataType = CO2
        refreshDisplay()
    elif key == ord('f') or key == ord('F'):
        # Display median PD on the cube
        selectedDataType = PD
        refreshDisplay()
    elif key == ord('w') or key == ord('W'):
        # Decrease year displayed by one year
        selectedYearIndex -= 1
        
        # Set minimum selection
        if selectedYearIndex < 0:
            selectedYearIndex = 0
        
        selectedYear = years[selectedYearIndex]
        refreshDisplay()
    elif key == ord('e') or key == ord('E'):
        # Increase year displayed by one year
        selectedYearIndex += 1
        
        # Set maximum selction
        if selectedYearIndex >= len(years):
            selectedYearIndex = len(years) - 1  
                   
        selectedYear = years[selectedYearIndex]
        refreshDisplay()
    elif key == ord('.') or key == ord('>'):
        # Zoom in
        scale += 1
        if scale <= scalingUpperLimit:
            scaleFactor += 1
        else:
            scale = scalingUpperLimit
        refreshDisplay()
    elif key == ord(',') or key == ord('<'):
        # Zoom out
        scale -= 1
        if scale >= scalingLowerLimit:
            scaleFactor -= 1
        else:
            scale = scalingLowerLimit
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
        if tiltAmount > 180:
            tiltAmount = 180
        setDisplayedContinentText()
        refreshDisplay()
    elif key == GLUT_KEY_DOWN:
        # Tilt down by 10 degrees
        tiltAmount -= TILT
        if tiltAmount < -180:
            tiltAmount = -180
        setDisplayedContinentText()
        refreshDisplay()
    elif key == GLUT_KEY_LEFT:
        # Pan to right by 10 degrees
        panAmount += PAN
        if panAmount > 180:
            panAmount = 180
        setDisplayedContinentText()
        refreshDisplay()
    elif key == GLUT_KEY_RIGHT:
        # Pan to left by 10 degrees
        panAmount -= PAN
        if panAmount < -180:
            panAmount = -180
        setDisplayedContinentText()
        refreshDisplay()

#
# DRAWING ABILITIES
#

def adjustLighting():
    r_xz = lightRange*cos(lightPhi*pi/180)
    y = LightRange*sin(LightPhi*pi/180)
    z = r_xz*cos(LightTheta*pi/180)
    x = r_xz*sin(LightTheta*pi/180)

    glLightfv( GL_LIGHT0, GL_DIFFUSE, GLfloat_3(1,1,1) )
    glLightfv( GL_LIGHT0, GL_AMBIENT, GLfloat_3(0,0,0) )
    glLightfv( GL_LIGHT0, GL_SPECULAR, GLfloat_3(1,1,1) )
    glLightfv( GL_LIGHT0, GL_POSITION, GLfloat_4(x,y,z,1) )
    glEnable( GL_LIGHT0)
    
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
    glLoadIdentity() 
    glTranslatef(0, 0, -6)
    glTranslate(0, 0, scaleFactor) # Zooming in and out
    glRotated(tiltAmount, 1, 0, 0) # Tilting
    glRotated(panAmount, 0, 1, 0) # Panning 
    glEnable(GL_TEXTURE_2D)
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

def drawColourBar():
    """
        Draws a colour bar that will help show the range of values of a
        selected continent and data type from yellow to red.
    """
    glDisable(GL_TEXTURE_2D) 
    glLoadIdentity() 
    glTranslate(3, -1.5, -6)  
    glColor4f(1, 1, 1, 1)
    
    glPushMatrix()
    
    # Linear function for colour value vs. position of line drawn
    cx1 = 1
    cx2 = 0
    cy1 = 0
    cy2 = 2
    m = (cy2 - cy1) / (cx2 - cx1)
    c = cy1 - m * cx1
    
    width = 0.5 # Width of entire colour bar
    
    cv = 0
    while cv <= 1:
        colourPosition = m * cv + c
        drawBarLine(width, colourPosition, cv)
        cv += 1/255 - 0.0015 # Add constant to control gap between bar lines
        
    drawArrow(currentArrowPosition, width)
    glColor4f(1, 1, 1, 1)
    
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()

def drawBarLine(width, i, g):
    """
        Draws a straight line that will be a building block for the entire
        colour bar.
    """
    glColor4f(1, g, 0, 1)
    glBegin(GL_LINES)
    glVertex2f(0, i)
    glVertex2f(width/2, i)
    glEnd()
    
def drawArrow(pos, width):
    """
        Draws an arrow next to the colour bar to indicate where the current
        value sits in the value range.
    """
    glColor4f(0, 1, 0, 1)
    glBegin(GL_LINES)
    glVertex2f(0, pos)
    glVertex2f(-width/2, pos)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex2f(0, pos)
    glVertex2f(-0.1, 0.1 + pos)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex2f(0, pos)
    glVertex2f(-0.1, -0.1 + pos)
    glEnd()
    glColor4f(1, 1, 1, 1) # Otherwise textures can't display properly!
    
def drawSelectionText():
    """
        Draws text on the screen to show the selected data type, year and
        value at those points, for a particular continent
    """
    glDisable(GL_TEXTURE_2D) 
    font = GLUT_BITMAP_HELVETICA_12
    
    glLoadIdentity() # Cannot rotate with cube!
    glTranslatef(0, 0, -6)
    glColor4f(1, 1, 1, 1.0) # Text will be white
    glPushMatrix()
    
    # Display selected data type
    glRasterPos2f(xTextPos, yTextPosC)
    for c in "Continent: " + selectedContinent:
        glutBitmapCharacter(font, ord(c))
        
    glRasterPos2f(xTextPos, yTextPosDT)
    for c in "Data Type: " + selectedDataType:
        glutBitmapCharacter(font, ord(c))
    
    # Display selected year
    glRasterPos2f(xTextPos, yTextPosY)
    for c in "Year: " + selectedYear:
        glutBitmapCharacter(font, ord(c))
    
    # Display the value of the data at the selected data type, year and continent
    glRasterPos2f(xTextPos, yTextPosV)
    for c in "Value: " + str(currentValue) + " " + units[selectedDataType]:
        glutBitmapCharacter(font, ord(c))
      
    glPopMatrix()
    
def drawDisplay():
    """ 
        Main drawing function for the program. 
    """
    global scaleFactor
    
    # Prepare to draw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
     
    # Start drawing the cube
    drawSelectionText()
    drawColourBar()
    
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

def refreshDisplay():
    """
        Update textures and drawings.
    """
    makeTextureSelection()
    setCurrentValue()
    setArrowPosition()
    setDisplayedContinentText()
    drawDisplay()
    
def fixateOnContinent(continent):
    """
        When a continent is selected, the cube rotates to show off said
        continent directly.
    """
    global panAmount, tiltAmount
    tiltAmount, panAmount = rotationalPositions[continent]
    refreshDisplay()

#
# PROGRAM STARTING POINT
# 
def main():
    global windowHandle, initialWidth, initialHeight
    global initialXPosition, initialYPosition, programTitle
    
    try: 
        # Start up GLUT
        glutInit("")
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(initialWidth, initialHeight)
        glutInitWindowPosition(initialXPosition, initialYPosition)
        windowHandle = glutCreateWindow(programTitle)
        glutFullScreen()
        
        # Set up direct navigation menu
        glutCreateMenu(continentMenu)
        glutAddMenuEntry("Africa", africaItem)
        glutAddMenuEntry("Asia", asiaItem)
        glutAddMenuEntry("Europe", europeItem)
        glutAddMenuEntry("North America", naItem)
        glutAddMenuEntry("Oceania", oceaniaItem)
        glutAddMenuEntry("South America", saItem)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        
        # Set up display, idle, resizing and mouse and keyboard handling functions
        glutDisplayFunc(drawDisplay)
        glutIdleFunc(drawDisplay)
        glutReshapeFunc(resizeWindow)
        glutKeyboardFunc(keyPresses)
        glutSpecialFunc(rotationControls) # For non-ASCII keys (i.e. arrow keys)
    except:
        print(START_ERROR)
        return 
    
    # Initialise OpenGL and run program (will be in full screen)
    startGL(initialWidth, initialHeight)
    print(WINDOW_OPEN)
    print(WELCOME)
    glutMainLoop()
    
main()