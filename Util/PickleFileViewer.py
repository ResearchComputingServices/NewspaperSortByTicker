import pandas as pd
import sys
import string
from colorama import Fore, Back, Style

import Util


ignoreList = ['N:INCO', 'ANN:ANN', 'AOL:AOL','PLUS:EPLUS', 'VIEW:VIEW', 'S:SPRINT', 'ADAM:ADAM', 'CR:CRANE', 'VANS:VANS', 'CA:CA', 
'B:BARNES', 'NICE:NICE', 'BEST:BEST', 'ANTM:ANTHEM', 'BP:BP', 'HOPE:HOPE', 'T:AT&T', 'OMG:OM', 'IMAX:IMAX', 'TIME:TIME', 'ITT:ITT', 
'BT:BT', 'SOS:SOS', 'LONG:ELONG', 'FOX:FOX', 'TNS:TNS', 'DPL:DPL', 'ROME:ROME', 'PMI:PMI', 'HOME:AT HOME', 'CME:CME', 'STEM:STEM', 
'TROY:TROY', 'CNE:CNE', 'PHC:PHC', 'AJAX:AJAX', 'IT:GARTNER','DSS:DSS', 'PCB:PCB', 'MSCI:MSCI', 'CRH:CRH', 'NCR:NCR', 'BHP:BHP', 
'USB:US', 'NWS:NEWS', 'CIA:CITIZENS', 'MUST:COLUMBIA', 'CBRE:CBRE', 'APA:APA', 'PALM:PALM', 'BCE:BCE', 'CSRA:CSRA', 'HOPE:HOPE', 
'SNAP:SNAP', 'GBS:GBS', 'PVH:PVH', 'ADT:ADT', 'EMC:EMC','TIME:TIME', 'UNIT:UNITI','USG:USG', 'LEAF:LEAF','FMC:FMC']


#ignoreList = []

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
pickleFilePath = '/home/nickshiell/storage/PickleJar/2016/December/file-70.pkl'

InspectPKLFile(pickleFilePath)