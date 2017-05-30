from country import Country
from worldStatistic import WorldStatistic
import statistics

class Continent(object):
    
    continentList = []
    def __init__(self, name):
        self.name = name
        self.countries = []
        
        self.medianTB = {}
        self.valuesTB = {}
        self.maxTB = 0
        self.minTB = 0  
        self.gradientTB = 0
        
        self.medianGDP = {}
        self.valuesGDP = {}
        self.maxGDP = 0
        self.minGDP = 0
        self.gradientGDP = 0
        
        self.medianCO2 = {}
        self.valuesCO2 = {}
        self.maxCO2 = 0
        self.minCO2 = 0
        self.gradientCO2 = 0
        
        self.medianPD = {}
        self.valuesPD = {}
        self.maxPD = 0 
        self.minPD = 0
        self.gradientPD = 0
        
        self.yearList = []
        self.fillYears()
        
    def getName(self):
        return self.name
    
    def getCountries(self):
        return self.countries
    
    def getCountryNames(self):
        return [c.getName() for c in self.getCountries()]
    
    def addCountry(self, country):
        
        self.countries.append(country)
        countryCount = len(self.countries)
        
        # Median calculations
        for y in self.yearList:
            valsTB = self.valuesTB[y]
            valsTB.append(country.getStatValue(1, y))
            self.valuesTB[y] = valsTB
            self.medianTB[y] = round(statistics.median(self.valuesTB[y]), 3)

            valsGDP = self.valuesGDP[y]
            valsGDP.append(country.getStatValue(2, y))
            self.valuesGDP[y] = valsGDP
            self.medianGDP[y] = round(statistics.median(self.valuesGDP[y]), 3)
            
            valsCO2 = self.valuesCO2[y]
            valsCO2.append(country.getStatValue(3, y))
            self.valuesCO2[y] = valsCO2
            self.medianCO2[y] = round(statistics.median(self.valuesCO2[y]), 3)
            
            valsPD = self.valuesPD[y]
            valsPD.append(country.getStatValue(4, y))
            self.valuesPD[y] = valsPD
            self.medianPD[y] = round(statistics.median(self.valuesPD[y]), 3)
        
        # Max values
        self.maxTB = max(self.medianTB.values())
        self.maxGDP = max(self.medianGDP.values())
        self.maxCO2 = max(self.medianCO2.values())
        self.maxPD = max(self.medianPD.values())
        
        # Min values
        self.minTB = min(self.medianTB.values())
        self.minGDP = min(self.medianGDP.values())
        self.minCO2 = min(self.medianCO2.values())
        self.minPD = min(self.medianPD.values())
        
    def getMedianTB(self, year):
        return self.medianTB[year]
    
    def getMedianGDP(self, year):
        return self.medianGDP[year]
    
    def getMedianCO2(self, year):
        return self.medianCO2[year]
    
    def getMedianPD(self, year):
        return self.medianPD[year]
    
    def getMaxValue(self, choice):
        if choice == 1:
            return self.maxTB
        elif choice == 2:
            return self.maxGDP
        elif choice == 3:
            return self.maxCO2
        else:
            return self.maxPD
    
    def getMinValue(self, choice):
        if choice == 1:
            return self.minTB
        elif choice == 2:
            return self.minGDP
        elif choice == 3:
            return self.minCO2
        else:
            return self.minPD
        
    def calculateGradient(self, choice, y1, y2):
        yDiff = y2 - y1
        xDiff = 0
        if choice == 1:
            xDiff = self.maxTB - self.minTB
        elif choice == 2:
            xDiff = self.maxGDP - self.minGDP
        elif choice == 3:
            xDiff = self.maxCO2 - self.minCO2
        else:
            xDiff = self.maxPD - self.minPD
        return yDiff / xDiff
        
    def getMedianValue(self, year, choice):
        if choice == 1:
            return self.getMedianTB(year)
        elif choice == 2:
            return self.getMedianGDP(year)
        elif choice == 3:
            return self.getMedianCO2(year)
        else:
            return self.getMedianPD(year)
    
    def getMedianValuesList(self, choice):
        if choice == 1:
            return self.medianTB.values()
        elif choice == 2:
            return self.medianGDP.values()
        elif choice == 3:
            return self.medianCO2.values()
        else:
            return self.medianPD.values()
             
    def fillYears(self):
        """ Loads up the year range used for
            storing average statistic values.
        """
        yearsFile = open('data/years.txt', 'r')
        years = yearsFile.readline()
        self.yearList = years.split(' ')
        for y in self.yearList:  
            self.medianTB[y] = 0
            self.valuesTB[y] = []
            self.medianGDP[y] = 0
            self.valuesGDP[y] = []
            self.medianCO2[y] = 0
            self.valuesCO2[y] = []
            self.medianPD[y] = 0
            self.valuesPD[y] = []
        yearsFile.close()
    
    def printStats(self):
        print("Countries in this continent:", [c.getName() for c in self.countries])
        print("Median TB:", self.medianTB)
        print("Median GDP:", self.medianGDP)
        print("Median CO2:", self.medianCO2)
        print("Median PD:", self.medianPD)
    
    def getStatisticNames():
        return ["TB", "GDP", "CO2", "PD"]
    
    def getYearList():
        return ["2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", 
        "2005", "2004"]
    
    #
    # Functions for generating a list of predefined continents for ease of
    # the user.
    #
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
        for y in Continent.getYearList():
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
        countries = Continent.fillCountries(countries)
        
        return countries
    
    def generateFullContinentList():
        continentMap = {}
        
        # Load continents
        continents = Continent.loadContinents()
        
        # Load countries and their data
        countries = Continent.loadCountries()
        
        # Add each country to 
        for co in continents:
            for c in countries:
                if c.getContinent() == co.getName():
                    co.addCountry(c)
    
        return continents
    
    
    