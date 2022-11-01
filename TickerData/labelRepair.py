def RepairName(brokenName):
    
    repairedName = ''
    
    nameSplit = brokenName.split(' ')
    
    cluster = ''
    clustering = False
    for item in nameSplit:
        item = item.strip()
        
        if len(item) == 1:
            cluster += item
            clustering = True
        elif clustering and len(item) != 1:
            repairedName += cluster + ' ' + item + ' '
            clustering = False
            cluster = ''
        else:           
            repairedName += item + ' '
            clustering = False
    
    if clustering and len(cluster) > 0:
        repairedName += cluster
    
    return repairedName


tickerDict = {}

outputFile = open('repairedTickers.csv','w+')

with open('tickers_company_names.csv', 'r') as inputFile:
    for line in inputFile:
        
        lineSplit = line.split(',')
        
        tickerLabel = lineSplit[0]
        companyName = RepairName(lineSplit[1])
        
        #print(line)
        #print(tickerLabel, ":", companyName)
        #input()
        
        outputFile.write(tickerLabel+','+companyName+'\n')
        