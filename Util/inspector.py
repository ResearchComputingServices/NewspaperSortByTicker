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

###################################################################################################
# Reads a PKL file and outputs the results when companies were found
###################################################################################################

def InspectPKLFile(pickleFilePath):

    pdf = pd.read_pickle(pickleFilePath)

    columnHeaders = pdf.columns

    for header in columnHeaders:
        print(header)

    nRows = len(pdf.index)
    print('# of Rows: ', nRows)

    input('Press ENTER to continue...')

    for iRow, row in pdf.iterrows():

        url = row['URL']
        title = row['Title']
        tickers = row['Ticker(s)']
        companyNames = row['CompanyNames']
        article = row['Article']
        index = row['TextIndex']
        searchTerms = row['SearchTerms']

        extractedArticle = row['CleanedArticle']
        extractedIndex = row['CleanedIndex']
        
        index = row['TextIndex']
        listOfKeys = list(index.keys())
        listOfKeys.sort()

        cleanedCompanyList = []
        foundCompanyNames = []
        foundCompanySymbol = []
        for name in companyNames:
            if not name.strip() in ignoreList:
                cleanedCompanyList.append(name)
                nameSplit = name.split(':')
                symbol = nameSplit[0].strip()
                companyName = nameSplit[1]
                foundCompanySymbol.append(symbol)
                companyName = companyName.split(' ')
                for word in companyName:
                    foundCompanyNames.append(word.lower().capitalize())
                

        highlightedArticle = ''                 
        article = article.split(' ')
        for word in article:       
                checkWord = word.translate(str.maketrans('', '', string.punctuation))
                if checkWord.strip() in foundCompanySymbol: 
                    highlightedArticle += ' ' + Fore.RED + word 
                elif checkWord.strip() in foundCompanyNames: 
                    highlightedArticle += ' ' + Fore.GREEN + word 
                else:
                    highlightedArticle += ' ' + Fore.WHITE + word
        """
        for name in cleanedCompanyList:
            nameSplit = name.split(':')    
            for word in article:       
                checkWord = word.translate(str.maketrans('', '', string.punctuation))
                if checkWord.strip() == nameSplit[0].strip(): 
                    highlightedArticle += ' ' + Fore.RED + word 
                else:
                    highlightedArticle += ' ' + Fore.WHITE + word
        """
        
        if len(cleanedCompanyList) > 0:
            print(highlightedArticle)    
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            for k in sorted(index): 
                print(k+"/ ", end='')
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            print('Symbols: ', tickers)
            print('Companies Found: ', cleanedCompanyList)
            print('Search Terms: ', searchTerms)
            print('Title:', title)
            print('URL:',url)
            print('Row: ', iRow,'/',nRows)
            print('\n================================================================================\n')    

            input('Press ENTER to continue...')
       
        """
        if len(cleanedCompanyList) > 0:
            #print(article)    
            print(highlightedArticle)    
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            #for k in sorted(index): 
            #    print(k+"/ ", end='')
            #print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
           # print(extractedArticle)
           # print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
           # for k in sorted(extractedIndex): 
           #     print(k+"/ ", end='')
           # print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            print('Symbols: ', tickers)
            print('Companies Found: ', cleanedCompanyList)
            print('Search Terms: ', searchTerms)
            print('Title:', title)
            print('URL:',url)
            print('Row: ', iRow,'/',nRows)
            print('\n================================================================================\n')    

            input()
        """
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
pickleFileDir = '/home/nickshiell/storage/TestSet/TestPickle/'
actionFlag = ''
if len(sys.argv) == 3:
    pickleFileDir = sys.argv[1]
    actionFlag = sys.argv[2]
else:
    print('ERROR: Too few/many command like args 2 were expected',len(sys.argv)-1, 'were recieved\n')
    sys.exit()

if actionFlag == 'c':
    CountResults(pickleFileDir)
elif actionFlag == 'i':
    InspectPKLFile(pickleFileDir)
else:
    print('Unknown action flag: ', actionFlag)
    sys.exit()