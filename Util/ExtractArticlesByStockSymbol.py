import sys
import os
import pandas as pd

import Util

############################################################################################################
# 
############################################################################################################
def SearchForRowForSymbol(row, symbol):
    searchResults = row['SEARCH_RESULTS']
    
    if len(searchResults) > 0:
        for item in searchResults:
            itemSplit = item.split(':')
            if itemSplit[0] == symbol:
                return True

    return False

############################################################################################################
# 
############################################################################################################
def SearchDataFrameForSymbol(pdf, symbol):
    
    indexList = []
            
    for index, row in pdf.iterrows():       
        if SearchForRowForSymbol(row,symbol):
            indexList.append(index)
    
    return indexList

############################################################################################################
# 
############################################################################################################
def SaveResults(indexList, pdf, symbol):
    
    outputFilePath = './Output/'+symbol+'.csv' 
    
    outputFile = open(outputFilePath, 'a+')
    
    for index in indexList:
        row = pdf.iloc[index]

        cleanedArticle = Util.CleanWhiteSpace(row['Article'])
        
        foundAt = cleanedArticle.find(symbol)
                
        outputString =  str(row['TimeStamp']) + ',' +  \
                        str(row['URL']) + ',' + \
                        str(row['Title']) + ',' + \
                        cleanedArticle.strip() + ',' + \
                        str(foundAt) + '\n'
        
        outputFile.write(outputString)
         
############################################################################################################
# This searches a given pickle file for instances of the stock symbols and saves the output
############################################################################################################        
def HandlePickleFile(pickleFilePath, symbolList):
    print('Searching in: ', pickleFilePath)
    pdf = pd.read_pickle(pickleFilePath)
    print(pdf.keys())
    
    for symbol in symbolList:
        print('Searching for:', symbol)
        indexList = SearchDataFrameForSymbol(pdf, symbol)
        SaveResults(indexList, pdf, symbol)      
              
############################################################################################################
# This searches a folder full of pickle files
############################################################################################################  
def HandleFolderOfPickleFiles(folderPath, symbolList):
    listOfFiles = Util.listdir_nohidden(folderPath)

    for filename in listOfFiles:
        pickleFilePath = os.path.join(folderPath, filename)
        HandlePickleFile(pickleFilePath, symbolList)

############################################################################################################
# Test Function:
############################################################################################################
def TestFunction():
    monthList = ['August', 'December', 'November', 'October', 'September']
    pickleFileDir = '/home/nickshiell/storage/BaChu/PickleJar/2016/'
    tickerDictFilePath = '../TickerData/tickersCompanyNames.csv'
   
    symbolList = Util.ReadTickerFile(tickerDictFilePath)

    for month in monthList:
        print('Month: ', month)
        searchLocation = os.path.join(pickleFileDir, month)
        HandleFolderOfPickleFiles(searchLocation, symbolList)
        


