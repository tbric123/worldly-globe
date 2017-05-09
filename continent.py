from country import Country

class Continent(object):
    
    def __init__(self, name):
        self.name = name
        self.countries = []
        self.averageTB = {}
        self.averageGDP = {}
        self.averageCO2 = {}
        self.averagePD = {}
    
    def getName(self):
        return self.name
    
    def addCountry(self, country):
        self.countries.append(country)
        
