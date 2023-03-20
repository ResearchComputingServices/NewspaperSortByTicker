import string
from colorama import Fore, Back, Style
import sys
import re
import pandas as pd
from typing import List
from dataclasses import dataclass, field
from time import sleep

from nltk.corpus import stopwords
from urllib.parse import urlsplit, urlunsplit

import Util

############################################################################################################
# This data class is used to consolidate the data required to do the multi-level search
############################################################################################################
@dataclass
class SearchSeed:
    bracket: str = ''                                           # bracket that acts as the seed for an indepth search
    bracketIndex: int = -1                                      # the location with in the article that the bracket was found
    foundSymbolsList: List = field(default_factory=lambda: [])  # a list of all the stock symbols found in the bracketed text
    subString: str = ''                                         # substring from the article before the bracket used to find the company name
    subStringIndex = -1                                         # starting location of the substring
    companyName: str = ''                                       # name of found company
    companySymbol: str = ''                                     # symbol of found company

############################################################################################################
# This function removes common suffixes from the company name and removes any white spaces
############################################################################################################

def CleanCompanyName(companyName):
    
    cleanName = ''
           
    nameSplit = companyName.split(' ')
    
    for suf in Util.companySuffixes:
        if suf in nameSplit:
            nameSplit.remove(suf)
    
    for item in nameSplit:
        cleanName += item + ' '
    
          
    return cleanName.strip()

############################################################################################################
# This function reads in the stock symbol data
############################################################################################################
def ReadTickers(stockListFilePath, verbose=False):
    
    tickerList = {}
    counter = 1

    with open(stockListFilePath, 'r') as inputFile:
        for line in inputFile:          
            lineSplit = line.strip().split(',')
            ticker = lineSplit[0]
            companyName = lineSplit[1]
            
            # expand these short forms in the company names
            companyName = companyName.replace('INTL', 'International')
            companyName = companyName.replace('INDS', 'Industries')
            companyName = companyName.replace('MFG', 'Manufacturing')
                        
            if ticker not in tickerList:
                tickerList[ticker] = companyName
            else:
                if verbose:
                    print(counter,' Duplicate: ', line.strip(), '//', ticker,',',tickerList[ticker] )
                    counter += 1
   
    if verbose:
        for idx,key in enumerate(tickerDict):   
            print(idx,':',key,':',tickerDict[key])
    
            if (idx+1) % 5 == 0:
                input()
       
    return tickerList

############################################################################################################
# This function removes common words (stop words) from the text passed in as an argument
############################################################################################################
def RemoveStopWords(text):  
    swList = stopwords.words('english')

    cleanedText = ''
    for word in text.split(' '):
        if word.lower() not in swList:
            addWord = word
           
            cleanedText += addWord + ' '
    
    return cleanedText

############################################################################################################
# This function cleans up excess whitespaces in the article
############################################################################################################
def CleanWhiteSpace(article):
    cleanedArticle = article

    # this like replaces multiple white space with a single space
    cleanedArticle = re.sub(' +', ' ', cleanedArticle)

    # this replaces all '( ' with a sinlge '('
    cleanedArticle = re.sub('\( ', '(', cleanedArticle)
    
    # this replaces all ' )' with a sinlge ')'
    cleanedArticle = re.sub(' \)', ')', cleanedArticle)

    return cleanedArticle

############################################################################################################
# This function searches for the name of a company near the location in the text where the symbol was found
############################################################################################################
def GetSubString(index, companyName, article, BUFFER = 5, MIN_LENGTH = 25 ):
   
    companyNameLength = len(companyName)+BUFFER
    if companyNameLength < MIN_LENGTH: companyNameLength = MIN_LENGTH
    
    startIndex = index - companyNameLength
    if startIndex < 0 : startIndex = 0
    endIndex = index - 1 
    subArticle = article[startIndex:endIndex]
    
    subArticle = RemoveStopWords(subArticle)             
    subArticle = re.sub(r'[^\w\s]', '', subArticle)
    
    return subArticle, startIndex, endIndex   

############################################################################################################
# This function finds all the text enclosed by brackets and then searches the contents for stock symbols
############################################################################################################
def StockSymbolSearch(article, tickerDict, searchSeedList):
          
    # search the article for text enclosed by brackets
    brackets = []
    brackets = re.findall('\(.*?\)',article)

    # add the found brackets to the searchSeedList
    for b in brackets:
        index = article.find(b)
        seed = SearchSeed(bracket=b,bracketIndex=index)
        searchSeedList.append(seed)
                        
    for seed in searchSeedList:
        # remove the brackets and split the text by common delims
        contents = re.split('\:| |\.',seed.bracket[1:-1])

        for token in contents:
            if len(token.strip()) == 0: continue
            
            if token in tickerDict.keys():
                seed.foundSymbolsList.append(token)
    
############################################################################################################
# This function searches for the name of a company near the location in the text where the symbol was found
############################################################################################################
def CompanyNameSearch(article, tickerDict, searchSeedList):

    for seed in searchSeedList:
        if len(seed.foundSymbolsList) == 0: continue
        
        # we only car about the first symbol found
        symbol = seed.foundSymbolsList[0]
        
        # get the company name, then clean and split it
        companyName = tickerDict[symbol]           
        companyNameClean = CleanCompanyName(companyName)
                
        # Get the substring at least 10 characters long
        subString, startIndex, endIndex = GetSubString( seed.bracketIndex, 
                                                        companyName, 
                                                        article)
        
        seed.subString = subString
        seed.subStringIndex = startIndex
        
        subString = subString.lower()
        # search fot parts of the company name in the substring before the brackets
        companySplit = companyNameClean.split(' ')
        # Now search the substring for any parts of the company name
        for token in companySplit:      
            if token.lower() in subString.split(' '):
                seed.companySymbol = symbol
                seed.companyName = companyName
                break       

############################################################################################################
# This function searches a specific row in a data frame
############################################################################################################
def Display(iRow, row, article, searchSeedList):
    bracketList = []              
    foundSymbolList = []      
    foundCompanyList = []
    
    url = row['URL']
    title = row['Title']
    
    for seed in searchSeedList:
     
        if not seed.bracket in bracketList:
            bracketList.append(seed.bracket)
        
        if len(seed.foundSymbolsList) > 0:
            if not seed.foundSymbolsList[0] in foundSymbolList:
                foundSymbolList.append(seed.foundSymbolsList[0])
            
        
        if seed.companyName == '':
            index = article.find(seed.bracket)
            length = len(seed.bracket)
            
            article =   article[:index] + \
                        Fore.CYAN + article[index:index+length] + \
                        Fore.WHITE + article[index+length:]
        else:
            index = article.find(seed.bracket)
            lengthBracket = len(seed.bracket)
            article =   article[:index] + \
                        Fore.RED + article[index:index+lengthBracket] + \
                        Fore.WHITE + article[index+lengthBracket:]     
            
            lengthSubString = len(seed.subString)
            index = index - lengthSubString
            if index >= 0:
                article =   article[:index] + \
                            Fore.GREEN + article[index:index+lengthSubString] + \
                            Fore.WHITE + article[index+lengthSubString:]
                            
            foundString = seed.companySymbol+':'+seed.companyName
            if not foundString in foundCompanyList:
                foundCompanyList.append(foundString)
            
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    print(article)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    print('Row #: ', iRow)
    print('Title:', title)
    print('URL:', url)
    print('BRACKETS: ', bracketList)
    print('FOUND SYMBOL:', foundSymbolList)
    print('FOUND COMPANY:', foundCompanyList)
    input('Press ENTER to continue...')

############################################################################################################
# This function searches a specific row in a data frame
############################################################################################################
def SearchRow(iRow, row, tickerDict, VERBOSE = False):
        
    searchSeedList = []
            
    # Get data from the dataframe
    article = row['Article']

    # Clean the article by removing excess white space
    article = CleanWhiteSpace(article)
   
    # Find all bracketed text and identify those containing stock symbols
    StockSymbolSearch(article,tickerDict, searchSeedList)
                           
    # Search for company names in the text immediatelt before the brackets with symbols 
    CompanyNameSearch(article, tickerDict, searchSeedList)
        
    # Determine if at least one company has been found
    foundCompany = False
    for seed in searchSeedList:
        if len(seed.companyName) > 0:
            foundCompany = True
            break
    
    # Display results  
    if foundCompany and VERBOSE:
        Display(iRow, row, article, searchSeedList)
    
                    
    return searchSeedList

############################################################################################################
# This function adds a new column to the dataframe which contains the found company name symbols 
# and their associate bracket
############################################################################################################ 
def AppendResultsToDataFrame(pdf, searchSeedList, iRow, columnName = 'SEARCH_RESULTS'):
           
    # Create a list of symbol:name for each company found
    foundCompanyList = []
    for seed in searchSeedList:
        if len(seed.companyName) > 0:
            foundCompanyList.append(seed.companySymbol+':'+seed.companyName+':'+seed.bracket)
    
    pdf.loc[iRow][columnName] = foundCompanyList
    
        
    return pdf
      
############################################################################################################
# This function opens a PKL as a pandas dataframe and searches it row by row for references to stocks
# the function appends a column to the dataframe which contains the found references
############################################################################################################
def SearchPKLFile(filePath,tickerDict, columnName = 'SEARCH_RESULTS', VERBOSE = False):
    
    pdf = pd.read_pickle(filePath)

    # add the 'SEARCH_RESULTS' column to the data frame
    pdf[columnName] = ''

    for iRow, row in pdf.iterrows():
        searchSeedList = SearchRow(iRow, row, tickerDict, VERBOSE=VERBOSE)
        pdf = AppendResultsToDataFrame(pdf, searchSeedList, iRow)
            
    return pdf
    
############################################################################################################
# Test Function:
############################################################################################################
def TestFunction():
    monthList = ['August', 'December', 'November', 'October', 'September']
    pickleFileDir = '/home/nickshiell/storage/TestSet/PickleJar/2016/'
    tickerDictFilePath = '../TickerData/tickersCompanyNames.csv'

    tickerDict = ReadTickers(tickerDictFilePath)

    VERBOSE = True

    for month in monthList:
        
        print('Month: ', month)
        
        searchLocation = pickleFileDir+month+'/'
        listOfFiles = Util.listdir_nohidden(searchLocation)

        for filename in listOfFiles:
            print('Filename: ', filename)
            filePath = searchLocation + filename
            pdf = SearchPKLFile(filePath, tickerDict, VERBOSE=VERBOSE)
            pdf.to_pickle(filePath)
            
    sys.exit()

############################################################################################################
# This function inspects the results of the search
############################################################################################################ 
def InspectPKLFile(filePath):
    pdf = pd.read_pickle(filePath)

    print(pdf.columns)

    for iRow, row in pdf.iterrows():          
        if len(row['SEARCH_RESULTS']) > 0:
            print(iRow,':',row['SEARCH_RESULTS'])
            input('Press ENTER to continue...')

############################################################################################################
# Production Run:
############################################################################################################  
def ProductionRun(pickleFilePath, tickerDictFilePath, VERBOSE = False):
    
    print(pickleFilePath)
    listOfFiles = Util.listdir_nohidden(pickleFilePath)

    tickerDict = ReadTickers(tickerDictFilePath)

    for filename in listOfFiles:
        filePath = pickleFilePath + filename
        pdf = SearchPKLFile(filePath, tickerDict, VERBOSE=VERBOSE)       

        if VERBOSE:        
            for iRow, row in pdf.iterrows():          
                if len(row['SEARCH_RESULTS']) > 0:
                    print(iRow,':',row['SEARCH_RESULTS'])
                    input('Press ENTER to continue...')

        pdf.to_pickle(filePath) 
    
    sys.exit()

TestFunction()