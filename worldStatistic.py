class WorldStatistic(object):
    """
        A statistic about a particular country/continent
    """
    def __init__(self, name, value, units):
        self.name = name
        self.value = value
        self.units = units
    
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value
    
    def getUnits(self):
        return self.units
    
    def __str__(self):
        return self.name + ": " + str(self.value) + " " + self.units

if __name__ == "__main__":
    ws = WorldStatistic("TB Mortality", 40, "people/capita")
    print(ws)
