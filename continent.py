from country import Country
from worldStatistic import WorldStatistic

class Continent(object):
    
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
        
if __name__ == '__main__':
    
    # Intro
    years = ['2013', '2012', '2011', '2010']
    types = ['TB', 'GDP', 'CO2', 'PD']
    units = ['people/capita', '$US/capita', 'tonnes/capita', 'people/km^2']
    
    
    tb1 = [0.1, 0.2, 0.3, 0.4]
    tb2 = [0.05, 0.06, 0.07, 0.08]
    gdp1 = [50000, 40000, 30000, 20000]
    gdp2 = [60000, 55000, 50000, 45000]
    co21 = [0.01, 0.02, 0.03, 0.04]
    co22 = [0.05, 0.04, 0.04, 0.03]
    pd1 = [4000, 3000, 2000, 1000]
    pd2 = [5000, 4000, 3000, 2000]
    
    fStats = [tb1, gdp1, co21, pd1]
    gStats = [tb2, gdp2, co22, pd2]
    
    # Form continent
    europe = Continent('Europe')
    
    # Form countries
    france = Country('France', 'Europe')
    germany = Country('Germany', 'Europe')
    
    for i in range(len(years)):
        for j in range(len(years)):
            france.addStat(i + 1, years[j], WorldStatistic(types[i], fStats[i][j], 
                           units[i]))
            germany.addStat(i + 1, years[j], WorldStatistic(types[i], gStats[i][j], 
                           units[i]))
    print("------------------")
    europe.addCountry(france)
    print("------------------")
    europe.printStats()
    print("------------------")
    europe.addCountry(germany)
    europe.printStats()
    print("------------------")
    
    
    
    
    
    
    