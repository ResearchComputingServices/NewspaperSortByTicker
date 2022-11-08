import pandas
import os
import sys
import time

import Util

##########################################################################################################
# This function searches for instances of COMPANY NAMES in the ARTICLE stored in the pandas data frame
##########################################################################################################
def CleanCompanyName(companyName):
    
    cleanName = ''
    
    nameSplit = companyName.split(' ')
    
    for suf in Util.companySuffixes:
        if suf in nameSplit:
            nameSplit.remove(suf)
    
    for item in nameSplit:
        cleanName += item + ' '
       
    return cleanName.strip()

def SearchForCompanyNameInArticlePDF(pdf, tickerAndCompanyList, DEBUG = False):  

    pdf['CompanyNames'] = ''
    pdf['SearchTerms'] = ''

    for iRow, row in pdf.iterrows():
        
        articleText = row['Article']
        tickerList = row['Ticker(s)']

        foundCompanyList = []
        searchTermsList = []
        for ticker in tickerList:
            companyName = tickerAndCompanyList[ticker]

            searchTermsList.append(ticker+':'+companyName)

            # Company names look for lower case
            if companyName.lower() in articleText.lower():
                foundCompanyList.append(companyName)
                
                

        pdf.loc[iRow]['CompanyNames'] = foundCompanyList
        pdf.loc[iRow]['SearchTerms'] = searchTermsList
    return pdf


##########################################################################################################
# This function searches for instances of tickerList elements in the pandas data frame
##########################################################################################################
def SearchForTickersInIndexPDF(pdf, tickerAndCompanyList, DEBUG = False):

    pdf['Ticker(s)'] = ''
       
    nRows = len(pdf.index)
    for iRow, row in pdf.iterrows():
        if DEBUG:
            print(iRow, " / ", nRows)
        
        textIndex = row['TextIndex']
               
        if DEBUG:
            print(textIndex)

        foundTickerList = []
        for key in tickerAndCompanyList.keys():
            tickerFound = False
            
            ticker = key
            
            # tickers should be ALL capitalized
            if ticker in textIndex.keys():
                tickerFound = True               
           
            if tickerFound:
                foundTickerList.append(ticker)  

        pdf.loc[iRow]['Ticker(s)'] = foundTickerList
        
        if DEBUG and len(foundTickerList) > 0:
            print(pdf.loc[iRow]['Title'], ': ', pdf.loc[iRow]['Ticker(s)'])
        
        if DEBUG:
            input()
        
    return pdf

##########################################################################################################
#  This function opens a .pkl file and searches it for instances of tickerList elements
##########################################################################################################

def SearchForTickersInIndexPKL(pickleFilePath, tickerList, DEBUG=False):

    print('Searching: ', pickleFilePath)
    
    df = pandas.read_pickle(pickleFilePath)  
    
    SearchForTickersInIndexPDF(df, tickerList, DEBUG)

    return df

##########################################################################################################
# This function is just a helper for the main code. It reads the tickerList from a file
##########################################################################################################

def ReadTickers(stockListFilePath):
    
    tickerList = []
    tickerAndCompanyDict = {}

    with open(stockListFilePath, 'r') as inputFile:
        for line in inputFile:          
            lineSplit = line.strip().split(',')
            ticker = lineSplit[0]
            company =  CleanCompanyName(lineSplit[1])
            
            if ticker not in tickerAndCompanyDict.keys():
                tickerAndCompanyDict[ticker] = company
   
    return tickerAndCompanyDict

##########################################################################################################
# This function performs the two level search on a single Panda's Data Frame
##########################################################################################################
def TickerSorterPandasDF(pdf, stockListFilePath):
    
    # get the ticker/company dict
    tickerAndCompanyDict = ReadTickers(stockListFilePath)

   
    # do initial sybmol only search of index
    pdf = SearchForTickersInIndexPDF(pdf,tickerAndCompanyDict)
   
    # use the found stock symbols to search for associated comapny names in ARTICLE
    pdf = SearchForCompanyNameInArticlePDF(pdf,tickerAndCompanyDict)
   
    return pdf

##########################################################################################################
# This function performs the two level search on a single PKL file
##########################################################################################################
def TickerSorterSinglePKLFile(filename, inputPickleFileDir, outputPickleFileDir, stockListFilePath):

    # This will be returned
    pdf = pandas.DataFrame()

    # make sure the directories have the right format (ie. end with /)
    inputPickleFileDir = Util.CheckDirectoryPath(inputPickleFileDir)
    outputPickleFileDir = Util.CheckDirectoryPath(outputPickleFileDir)
    
    # Check the correct type of file has been passed in
    if Util.ExtensionOnly(filename) != 'pkl':
         print('Invalid file type (only .pkl files): ', filename)
    else:
        # open and read the pickle file
        inputPickleFilePath = inputPickleFileDir + filename
        pdf = pandas.read_pickle(inputPickleFilePath)  
      
        # The actual sorting happens here
        pdf = TickerSorterPandasDF(pdf, stockListFilePath)
        
        # save results
        pdf.to_pickle(outputPickleFileDir + filename)
           
    return pdf

##########################################################################################################
# This function will searches all the Pickle files in a directory for instances of elements of the
# tickerList and save the results
##########################################################################################################

def TickerSorterProductionRun(inputPickleFileDir, outputPickleFileDir, stockListFilePath):

    inputPickleFileDir = Util.CheckDirectoryPath(inputPickleFileDir)
    outputPickleFileDir = Util.CheckDirectoryPath(outputPickleFileDir)

    listOfFiles = Util.listdir_nohidden(inputPickleFileDir)
    tickerAndCompanyList = ReadTickers(stockListFilePath)

    print("SEARCHING FOR TICKERS:")
    print("Input Data: ", inputPickleFileDir)
    print("Stock List: ", stockListFilePath)
    print("Output Data: ", outputPickleFileDir)
    print('# of tickers: ', len(tickerAndCompanyList))
    print('# of files: ', len(listOfFiles))

    for filename in listOfFiles:
        TickerSorterSinglePKLFile(filename, inputPickleFileDir, outputPickleFileDir, tickerAndCompanyList)
