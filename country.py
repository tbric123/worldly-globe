class Country(object):
    
    def __init__(self, name, continent):
        self.name = name
        self.continent = continent
        self.tbmStats = {}
        self.gdpStats = {}
        self.co2Stats = {}
        self.pdStats = {}
        self.fillYears()
        
    def getName(self):
        return self.name
    
    def getContinent(self):
        return self.continent
    
    def __str__(self):
        return "Country: " + self.name
    
    def addStat(self, statType, year, value):
        """ Add a statistic to any of the country's statistics.
            statType values:
                1 - TBM
                2 - GDP
                3 - CO2
                4 - PD
        """
        if statType == 1:
            self.tbmStats[year] = value
        elif statType == 2:
            self.gdpStats[year] = value
        elif statType == 3:
            self.co2Stats[year] = value
        elif statType == 4:
            self.pdStats[year] = value
    
    def getStats(self, statType):
        if statType == 1:
            return self.tbmStats
        elif statType == 2:
            return self.gdpStats
        elif statType == 3:
            return self.co2Stats
        else:
            return self.pdStats
    
    def getStatValue(self, statType, year):
        stats = {}
        
        if statType == 1:
            stats = self.tbmStats
        elif statType == 2:
            stats = self.gdpStats
        elif statType == 3:
            stats = self.co2Stats
        else:
            stats = self.pdStats
        
        return stats[year]

    
    def fillYears(self):
        """ Loads up the year range used for
            storing average statistic values.
        """
        yearsFile = open('data/years.txt', 'r')
        years = yearsFile.readline()
        self.yearList = years.split(' ')
        for y in self.yearList:  
            self.tbmStats[y] = 0
            self.gdpStats[y] = 0
            self.co2Stats[y] = 0
            self.pdStats[y] = 0             
        yearsFile.close()
    
    def printStats(self):
        print("TB:")
        print([self.getStats(1)])
        print("***")
        print("GDP:")
        print([self.getStats(2)])
        print("***")
        print("CO2:")
        print([self.getStats(3)])
        print("***")
        print("PD:")
        print([self.getStats(4)])
        print("***")