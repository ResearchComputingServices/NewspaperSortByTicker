import sys

import pandas as pd
from colorama import Fore, Back, Style

import Util

###################################################################################################
# Displays a row from the pickle file
###################################################################################################

def Display(row, rowNumber):
   
    resultsList = row['SEARCH_RESULTS']
    article = row['Article']
    article = Util.CleanWhiteSpace(article)
    
    foundSymbolList = []      
    foundCompanyList = []
    
    for result in resultsList:
        symbol = result.split(':')[2]
        name = result.split(':')[1]
        foundSymbolList.append(symbol)
        foundCompanyList.append(name)
        
        index = article.find(symbol)
        length = len(symbol)
        
        article =   article[:index] + \
                    Fore.CYAN + article[index:index+length] + \
                    Fore.WHITE + article[index+length:]        
        
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    print(article)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    print('Row #: ', rowNumber)
    print('Title:', row['Title'])
    print('URL:', row['URL'])
    print('FOUND SYMBOL:', foundSymbolList)
    print('FOUND COMPANY:', foundCompanyList)
    print('ResultList:', resultsList)  

###################################################################################################
# Reads a PKL file and outputs the results when companies were found
###################################################################################################

def InspectPKLFile(pickleFilePath):

    pdf = pd.read_pickle(pickleFilePath)
    print('Searching: ', pickleFilePath)
    
    print(pdf.keys())   
    
    for iRow, row in pdf.iterrows():          
        if len(row['SEARCH_RESULTS']) > 0:
            Display(row, iRow)
            input('Press ENTER to continue...')

 
###################################################################################################
# This function searching all PKL files in the directory and records which company were found
# and how many times
###################################################################################################

def CountResults(pickleFileDir):

    listOfFiles = Util.listdir_nohidden(pickleFileDir)

    companyDict = {}

    for filename in listOfFiles:
    
        pdf = pd.read_pickle(pickleFileDir+'/'+filename)
        print('Searching: ', filename)
        nRows = len(pdf.index)
        for iRow, row in pdf.iterrows():
            companyNames = row['CompanyNames']
            if len(companyNames) > 0:   

                for name in companyNames:
                    if name in companyDict.keys():
                        companyDict[name] = companyDict[name] + 1
                    else:
                        companyDict[name] = 1

            if iRow % 250 == 0:
                print(iRow,'/',nRows)

    for key in companyDict.keys():
        print(key,',',companyDict[key])
    
    return companyDict
    
    
###################################################################################################
# interact with the above functions through interface below
###################################################################################################

pickleFilePath = ''

# example file path
# pickleFilePath = '/home/nickshiell/storage/BaChu/PickleJar/2016/December/file-70.pkl'

# Make sure that the command line args are present
if len(sys.argv) == 2:
    pickleFilePath = sys.argv[1]
else:
    print('[ERROR]: insufficient cmd line args: ', sys.argv)
    exit(0)

InspectPKLFile(pickleFilePath)