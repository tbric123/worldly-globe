from country import Country
from worldStatistic import WorldStatistic

class Continent(object):
    
    continentList = []
    def __init__(self, name):
        self.name = name
        self.countries = []
        
        self.averageTB = {}
        self.totalTB = {}
        
        self.averageGDP = {}
        self.totalGDP = {}
        
        self.averageCO2 = {}
        self.totalCO2 = {}
        
        self.averagePD = {}
        self.totalPD = {}
        
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
        
        # Totals calculation
        for y in self.yearList:
            self.totalTB[y] += round(country.getStatValue(1, y), 3)
            self.totalGDP[y] += round(country.getStatValue(2, y), 3)
            self.totalCO2[y] += round(country.getStatValue(3, y), 3)
            self.totalPD[y] += round(country.getStatValue(4, y), 3)
               
        # Update averages
        for y in self.yearList:
            self.averageTB[y] = round(self.totalTB[y] / countryCount, 3)
            self.averageGDP[y] = round(self.totalGDP[y] / countryCount, 3)
            self.averageCO2[y] = round(self.totalCO2[y] / countryCount, 3)
            self.averagePD[y] = round(self.totalPD[y] / countryCount, 3)  
           
    def getAverageTB(self, year):
        return self.averageTB[year]
    
    def getAverageGDP(self, year):
        return self.averageGDP[year]
    
    def getAverageCO2(self, year):
        return self.averageCO2[year]
    
    def getAveragePD(self, year):
        return self.averagePD[year]
    
    def getAverageValue(self, year, choice):
        if choice == 1:
            return self.getAverageTB(year)
        elif choice == 2:
            return self.getAverageGDP(year)
        elif choice == 3:
            return self.getAverageCO2(year)
        else:
            return self.getAveragePD(year)
    
    def getAverageValuesList(self, choice):
        if choice == 1:
            return self.averageTB.values()
        elif choice == 2:
            return self.averageGDP.values()
        elif choice == 3:
            return self.averageCO2.values()
        else:
            return self.averagePD.values()
             
    def fillYears(self):
        """ Loads up the year range used for
            storing average statistic values.
        """
        yearsFile = open('data/years.txt', 'r')
        years = yearsFile.readline()
        self.yearList = years.split(' ')
        for y in self.yearList:  
            self.averageTB[y] = 0
            self.totalTB[y] = 0
            self.averageGDP[y] = 0
            self.totalGDP[y] = 0
            self.averageCO2[y] = 0
            self.totalCO2[y] = 0
            self.averagePD[y] = 0
            self.totalPD[y] = 0             
        yearsFile.close()
    
    def printStats(self):
        print("Countries in this continent:", [c.getName() for c in self.countries])
        print("Avg TB:", self.averageTB)
        print("Total TB:", self.totalTB)
        print("Avg GDP:", self.averageGDP)
        print("Total GDP:", self.totalGDP)
        print("Avg CO2:", self.averageCO2)
        print("Total CO2:", self.totalCO2)
        print("Avg PD:", self.averagePD)
        print("Total PD:", self.totalPD)
    
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
    
    
    