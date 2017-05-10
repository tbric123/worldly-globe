from country import Country

class Continent(object):
    
    def __init__(self, name):
        self.name = name
        self.countries = []
        self.averageTB = {}
        self.averageGDP = {}
        self.averageCO2 = {}
        self.averagePD = {}
        
        self.fillYears()
        
    def getName(self):
        return self.name
    
    def addCountry(self, country):
        self.countries.append(country)
    
    def fillYears(self):
        """ Loads up the year range used for
            storing average statistic values.
        """
        yearsFile = open('data/years.txt', 'r')
        years = yearsFile.readline()
        yearList = years.split(' ')
        for y in yearList:  
            print(y)
            self.averageTB[y] = 0
            self.averageGDP[y] = 0
            self.averageCO2[y] = 0
            self.averagePD[y] = 0   
                          
        yearsFile.close()
        print(self.averageTB['2013'])
        
if __name__ == '__main__':
    europe = Continent('Europe')