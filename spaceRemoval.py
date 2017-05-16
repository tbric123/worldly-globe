def separateData(separator, dataFile, outFileName):
    outputFile = open(outFileName, 'w')
    for line in dataFile.readlines():
        line = line.replace("\t", separator) 
        line = line.replace(" ", separator)
        outputFile.write(line)

    outputFile.close()

inputFile = open("data/data.txt")
separateData("|", inputFile, "data/allData2004.txt")
inputFile.close()
