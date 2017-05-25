def combineFileLines(file1, file2, identifier):
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    f1Lines = f1.readlines()
    f2Lines = f2.readlines()

    asiaCount = 0
    asiaTBSum = 0
    asiaGDPSum = 0
    asiaCO2Sum = 0
    asiaPDSum = 0
    
    africaCount = 0
    africaTBSum = 0
    africaGDPSum = 0
    africaCO2Sum = 0
    africaPDSum = 0
    
    saCount = 0
    saTBSum = 0
    saGDPSum = 0
    saCO2Sum = 0
    saPDSum = 0
    
    naCount = 0
    naTBSum = 0
    naGDPSum = 0
    naCO2Sum = 0
    naPDSum = 0
    
    europeCount = 0
    europeTBSum = 0
    europeGDPSum = 0
    europeCO2Sum = 0
    europePDSum = 0
    
    oceaniaCount = 0
    oceaniaTBSum = 0
    oceaniaGDPSum = 0
    oceaniaCO2Sum = 0
    oceaniaPDSum = 0

    for i in range(0, len(f1Lines)):
        f1LineParts = f1Lines[i].strip().split("|")
        f2LineParts = f2Lines[i].strip().split("|")
        con = f1LineParts[1]
        nums = f2LineParts[1]
        
        tb = float(nums[0])
        print(nums[0])
        print(nums[1])
        print(nums[2])
        gdp = float(nums[1])
        co2 = float(nums[2])
        print(nums[3])
        pd = float(nums[3])
        
        if con == "Asia":
            asiaCount += 1
            asiaTBSum += tb
            asiaGDPSum += gdp
            asiaCO2Sum += co2
            asiaPDSum += pd
        elif con == "Africa":
            africaCount += 1
            africaTBSum += tb
            africaGDPSum += gdp
            africaCO2Sum += co2
            africaPDSum += pd
        elif con == "South America":
            saCount += 1
            saTBSum += tb
            saGDPSum += gdp
            saCO2Sum += co2
            saPDSum += pd
        elif con == "North America":
            naCount += 1
            naTBSum += tb
            naGDPSum += gdp
            naCO2Sum += co2
            naPDSum += pd
        elif con == "Europe":
            europeCount += 1
            europeTBSum += tb
            europeGDPSum += gdp
            europeCO2Sum += co2
            europePDSum += pd
        elif con == "Oceania":
            oceaniaCount += 1
            oceaniaTBSum += tb
            oceaniaGDPSum += gdp
            oceaniaCO2Sum += co2
            oceaniaPDSum += pd

    print("Asia", asiaCount, "Europe", europeCount, "South America", saCount,
          "North America", naCount, "Oceania", oceaniaCount, "Africa", africaCount)
    print("Averages for TB:")
    print("Asia", asiaTBSum/asiaCount, "Europe", europeTBSum/europeCount, "South America", saTBSum/saCount,
          "North America", naTBSum/naCount, "Oceania", oceaniaTBSum/oceaniaCount, "Africa", africaTBSum/africaCount)
    print("Averages for GDP:")
    print("Asia", asiaGDPSum/asiaCount, "Europe", europeGDPSum/europeCount, "South America", saGDPSum/saCount,
          "North America", naGDPSum/naCount, "Oceania", oceaniaGDPSum/oceaniaCount, "Africa", africaGDPSum/africaCount)
    print("Averages for CO2:")
    print("Asia", asiaCO2Sum/asiaCount, "Europe", europeCO2Sum/europeCount, "South America", saCO2Sum/saCount,
          "North America", naCO2Sum/naCount, "Oceania", oceaniaCO2Sum/oceaniaCount, "Africa", africaCO2Sum/africaCount)
    print("Averages for PD:")
    print("Asia", asiaPDSum/asiaCount, "Europe", europePDSum/europeCount, "South America", saPDSum/saCount,
          "North America", naPDSum/naCount, "Oceania", oceaniaPDSum/oceaniaCount, "Africa", africaPDSum/africaCount)
    f1.close()
    f2.close()
    
combineFileLines("countries.txt", "allData2013.txt", "2013")
