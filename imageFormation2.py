from PIL.Image import *
from continent import Continent

class ContinentImageCreator(object):
    
    def calculateColourGradient(allValues):
        # Treat as a linear function: y = mx + c
        x1 = min(allValues)
        x2 = max(allValues)
        y1 = 255
        y2 = 0
        m = (y2 - y1) / (x2 - x1)
        
        return m
    
    def calculateGreenChannel(xValue, m):
        """
            Calculate the value used for the green colour
            channel that will result in an image colour between
            yellow (minimum x value) and red (maximum x value).
            Sets y values to be between 0 and 255.      
        """
        
        # No floats for colour channels
        return int(m * xValue + 255) 
    
    
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
            valuesList = continent.getAverageValuesList(f)
            gradient = ContinentImageCreator.calculateColourGradient(valuesList)
            for y in years:
                savedName = "maps/" + continent.getName() + dataTypeNames[f - 1] + y + ".bmp"
                value = continent.getAverageValue(y, f)
                value = ContinentImageCreator.calculateGreenChannel(value, gradient)
                ContinentImageCreator.generateImage(value, originalName, savedName)

if __name__ == "__main__":
    continentList = Continent.generateFullContinentList()
    print(continentList)
    
    for c in continentList:
        ContinentImageCreator.createAllImages(c)