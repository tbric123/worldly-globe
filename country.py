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
    
    def addStat(self, statType, year, stat):
        """ Add a statistic to any of the country's statistics.
            statType values:
                1 - TBM
                2 - GDP
                3 - CO2
                4 - PD
        """
        if statType == 1:
            self.tbmStats[year] = stat
        elif statType == 2:
            self.gdpStats[year] = stat
        elif statType == 3:
            self.co2Stats[year] = stat
        elif statType == 4:
            self.pdStats[year] = stat
    
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
        
        return stats[year].getValue()
    
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
        
if __name__ == '__main__':
    from worldStatistic import WorldStatistic
    
    tbmStat = WorldStatistic('TB', 40, 'people/capita')
    gdpStat = WorldStatistic('GDP', 23, '$US/capita')
    co2Stat = WorldStatistic('CO2', 0.1, 'tonnes per capita')
    pdStat = WorldStatistic('PD', 200, 'people per km^2')
    tbmStat2 = WorldStatistic('TB', 50, 'people/capita')
    
    cambodia = Country("Cambodia", "Asia")
    print(cambodia)
    print(cambodia.getContinent())
    
    cambodia.addStat(1, '2013', tbmStat)
    print(cambodia.getStats(1)['2013'])
    print("---------")
    
    cambodia.addStat(2, '2013', gdpStat)
    print(cambodia.getStats(1)['2013'])
    print(cambodia.getStats(2)['2013'])
    print("---------")
    
    cambodia.addStat(3, '2013', co2Stat)
    print(cambodia.getStats(1)['2013'])
    print(cambodia.getStats(2)['2013'])
    print(cambodia.getStats(3)['2013'])
    print("---------")
    
    cambodia.addStat(4, '2013', pdStat)
    print(cambodia.getStats(1)['2013'])
    print(cambodia.getStats(2)['2013'])
    print(cambodia.getStats(3)['2013'])
    print(cambodia.getStats(4)['2013'])
    cambodia.addStat(1, '2012', tbmStat2)
    print(cambodia.getStats(1)['2013'])
    print(cambodia.getStats(1)['2012'])
  