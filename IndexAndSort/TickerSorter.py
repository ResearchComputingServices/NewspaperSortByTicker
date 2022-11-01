import pandas
import os
import sys
import time

import Util

##########################################################################################################
# This function searches for instances of tickerList elements in the pandas data frame
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


def SearchForTickersInPDF(pdf, tickerAndCompanyList, DEBUG):

    pdf['Ticker(s)'] = ''
       
    nRows = len(pdf.index)
    for iRow, row in pdf.iterrows():
        if DEBUG:
            print(iRow, " / ", nRows)
        
        textIndex = row['TextIndex']
               
        if DEBUG:
            print(textIndex)

        foundTickerList = []
        for entry in tickerAndCompanyList:
            stockFound = False
            tickerFound = False
            companyFound = False
            
            ticker = entry[0]
            company = CleanCompanyName(entry[1])
            
            # tickers should be ALL capitalized
            if ticker in textIndex.keys():
                tickerFound = True
                
            # Company names look for lower case
            for item in company.split(' '): 
                if item in textIndex.Keys():
                    companyFound = True
                else:
                    companyFound = False
                    break
            
            #if stockFound:
            #    foundTickerList.append(ticker)  
            if companyFound:
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

def SearchForTickersInPickleFile(pickleFilePath, tickerList, DEBUG=False):

    print('Searching: ', pickleFilePath)
    
    df = pandas.read_pickle(pickleFilePath)  
    
    SearchForTickersInPDF(df, tickerList, DEBUG)

    return df

##########################################################################################################
# This function is just a helper for the main code. It reads the tickerList from a file
##########################################################################################################

def ReadTickers(stockListFilePath):
    
    tickerList = []
    tickerAndCompanyList = []
    with open(stockListFilePath, 'r') as inputFile:
        for line in inputFile:          
            lineSplit = line.strip().split(',')
            ticker = lineSplit[0]
            company = lineSplit[1]
            entry = [ticker, company]
            # do this check to remove duplicates
            if not ticker in tickerList:
                tickerAndCompanyList.append(entry)
                tickerList.append(ticker)
   
    return tickerAndCompanyList

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

        # TODO: This check should be performed in the function
        if Util.ExtensionOnly(filename) == 'pkl':
            pdf = SearchForTickersInPickleFile(outputPickleFileDir + filename,tickerAndCompanyList)
            pdf.to_pickle(outputPickleFileDir + filename)
        else:
            print('Invalid file type (only .pkl files): ', filename)