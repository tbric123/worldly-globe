# Other modules
from time import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# My own modules
from worldStatistic import WorldStatistic
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
    glMatrixMode(GL_PROJECTION) # Set momentarily for view
    glLoadIdentity()
    gluPerspective(fov, float(width)/float(height), 0.1, 100)
    glMatrixMode(GL_MODELVIEW) # Allow for rotations and scaling

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

def exitProgram():
    """ 
        Quick function call for exiting the program.
    """
    glutDestroyWindow(windowHandle)
    sys.exit()

def loadContinents():
    continentFile = open('data/continents.txt')
    continents = []
    
    for c in continentFile.readlines():
        c = c.strip()
        continent = Continent(c)
        continents.append(continent)
    
    continentFile.close()
    return continents

def fillCountries(countries):
    print("Filling up each country with statistics...")
    log = open("data/log.txt", 'w')
    for y in years:
        dataFile = open('data/allData' + y + '.txt')
        dataContents = dataFile.readlines()
        countryCount = 0
        for c in countries:
           data = dataContents[countryCount].split("|")
           c.addStat(1, y, float(data[0]))
           c.addStat(2, y, float(data[1]))
           c.addStat(3, y, float(data[2]))
           c.addStat(4, y, float(data[3]))
           log.write(str(y) +  " TB stat for " + c.getName() + ": " + str(c.getStatValue(1, y)) + "\n")
           log.write(str(y) + " GDP stat for " + c.getName() + ": " + str(c.getStatValue(2, y)) + "\n")
           log.write(str(y) + " CO2 stat for " + c.getName() + ": " + str(c.getStatValue(3, y)) + "\n")
           log.write(str(y) + " PD stat for " + c.getName() + ": " + str(c.getStatValue(4, y)) + "\n")
           countryCount += 1
    print("Countries filled!")
    log.close()
    return countries

def loadCountries():
    countryFile = open('data/countries.txt')
    countries = []
    
    for line in countryFile.readlines():
        line = line.strip()
        information = line.split('|')
        country = Country(information[0], information[1])
        countries.append(country)
    
    countryFile.close()
    countries = fillCountries(countries)
    
    return countries

def loadAllData():
    continentMap = {}
    
    # Load continents
    continents = loadContinents()
    
    # Load countries and their data
    countries = loadCountries()
    
    # Add each country to 
    for co in continents:
        for c in countries:
            if c.getContinent() == co.getName():
                co.addCountry(c)

    return continents
 
def main():
    global windowHandle
    global initialWidth
    global initialHeight
    global initialXPosition
    global initialYPosition
    global programTitle
    global allData
    
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
    
    startGL(initialWidth, initialHeight)
    # Initialise OpenGL and run program
    print("Loading data...")
    allData = loadAllData()
    print(allData)
    print("Done.")
    print("Worldly Globe - press ESC or right-click window to exit program.")
        
    glutMainLoop()
    
main()
