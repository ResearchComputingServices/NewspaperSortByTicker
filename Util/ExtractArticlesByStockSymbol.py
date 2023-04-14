import sys
import os
import pandas as pd

import Util

############################################################################################################
# 
############################################################################################################
def AddSymbolsToDict(index, searchResults, symbolFoundDict):
    
    for item in searchResults:
        itemSplit = item.split(':')
        symbol = itemSplit[0]

        if symbol not in symbolFoundDict.keys():          
            symbolFoundDict[symbol] = []
        
        symbolFoundDict[symbol].append(index)

############################################################################################################
# 
############################################################################################################
def SaveResults(pdf, symbolFoundDict, outputDirPath, fileAccessType = 'a+'):
    
    # Loop over all the found symbols    
    for symbol in symbolFoundDict:
    
        # open the file with the correct name
        filename = symbol+'.csv'
        outputFilePath = os.path.join(outputDirPath,filename)
        outputFile = open(outputFilePath, fileAccessType)
        
        # get the list of rows which contain the symbol
        listOfRows = symbolFoundDict[symbol]
        
        # loop over the rows and add them to the file
        for index in listOfRows:
        
            row = pdf.iloc[index]

            cleanedArticle = Util.CleanWhiteSpace(row['Article'])
        
            foundAt = cleanedArticle.find(symbol)
                
            outputString =  str(row['TimeStamp']) + ',' +  \
                            str(row['URL']) + ',' + \
                            str(row['Title']) + ',' + \
                            cleanedArticle.strip() + ',' + \
                            str(foundAt) + '\n'
            
            outputFile.write(outputString)
    
        outputFile.close()
         
############################################################################################################
# This searches a given pickle file for instances of the stock symbols and saves the output
############################################################################################################        
def HandlePickleFile(pickleFilePath, outputDirPath):
    print('Searching in: ', pickleFilePath)
    pdf = pd.read_pickle(pickleFilePath)
    
    # this dictionary keeps track of which stock symbols were found on which rows of the data frame
    # key = symbol, value = list of rows indexs
    symbolFoundDict = {}
    
    for index, row in pdf.iterrows():    
        searchResults = row['SEARCH_RESULTS']
        if len(searchResults) > 0:
            AddSymbolsToDict(index, searchResults, symbolFoundDict)
        
    SaveResults(pdf, symbolFoundDict, outputDirPath)        
              
############################################################################################################
# This searches a folder full of pickle files
############################################################################################################  
def HandleFolderOfPickleFiles(folderPath, outputDirPath = './Output/'):
    listOfFiles = Util.listdir_nohidden(folderPath)

    for filename in listOfFiles:
        pickleFilePath = os.path.join(folderPath, filename)
        HandlePickleFile(pickleFilePath, outputDirPath)

############################################################################################################
# Test Function:
############################################################################################################
def TestFunction():
    monthList = ['August', 'December', 'November', 'October', 'September']
    pickleFileDir = '/home/nickshiell/storage/BaChu/PickleJar/2016/'
   
    for month in monthList:
        print('Month: ', month)
        searchLocation = os.path.join(pickleFileDir, month)
        HandleFolderOfPickleFiles(searchLocation)
        
############################################################################################################

# Uncomment the line of code below to run the TestFunction which demonstrates how the functions work.
#TestFunction()

