from PIL.Image import *
from continent import Continent

class ContinentImageCreator(object):
    
    def calculateColourGradientAndIntercept(con, choice):
        # Treat as a linear function: y = mx + c
        x1 = con.getMinValue(choice)
        x2 = con.getMaxValue(choice)
        y1 = 255
        y2 = 0
        m = (y2 - y1) / (x2 - x1) # Gradient
        c = y1 - m * x1 # Use an arbitrary x, y pair for y-intercept
        
        return m, c
    
    def calculateGreenChannel(xValue, m, c):
        """
            Calculate the value used for the green colour
            channel that will result in an image colour between
            yellow (minimum x value) and red (maximum x value).
            Sets y values to be between 0 and 255.      
        """
        
        # No floats for colour channels
        return int(m * xValue + c) 
    
    
    def generateImage(value, originalImage, savedImage):
        
        # Load blank map
        inputImage = open(originalImage)
        pixels = inputImage.load()
        
        # Colour the map
        for i in range(inputImage.size[0]):
            for j in range(inputImage.size[1]):
                if (pixels[i, j] != (0, 0, 255)):
                    pixels[i, j] = (255, value, 0)
        
        # Save and return newly coloured map
        inputImage.save(savedImage)
        return inputImage
    
    def createAllImages(continent):
        
        # Get years, data type getters and data type names directly from
        # Continent without an object being made from it
        years = Continent.getYearList()
        dataTypeFunctions = [1, 2, 3, 4]
        dataTypeNames = Continent.getStatisticNames()
        originalName = "maps/" + continent.getName() + "Blue.bmp"
        
        for f in dataTypeFunctions:
            valuesList = continent.getMedianValuesList(f)
            print(dataTypeNames[f - 1], ":", valuesList)
            
            gradient, intercept = ContinentImageCreator.calculateColourGradientAndIntercept(continent, f)
            
            for y in years:
                savedName = "maps/" + continent.getName() + dataTypeNames[f - 1] + y + ".bmp"
                value = continent.getMedianValue(y, f)
                colourValue = ContinentImageCreator.calculateGreenChannel(value, gradient, intercept)
                ContinentImageCreator.generateImage(colourValue, originalName, savedName)

if __name__ == "__main__":
    continentList = Continent.generateFullContinentList()    
    print("Creating images...")
    for c in continentList:
        print(c.getName(), ":")
        print([x.getName() for x in c.getCountries()])        
        ContinentImageCreator.createAllImages(c)
    print("Done!")