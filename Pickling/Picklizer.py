#import pandas
import os
import re
import fnmatch
from xmlrpc.client import FastUnmarshaller
import pandas as pd

import Util

########################################################################
# Function that looks through all the rows to make sure there are no 
# errors. If there are it tries to fix them
#######################################################################
def SanitizeDataRows(dataRows):
                          
    iRow = 0
    while iRow < len(dataRows)-1:
        curRow = dataRows[iRow]
        nextRow = dataRows[iRow+1]
        
        # check that the nextRow starts with a datestamp if not the data is corrupted and we need to merge the rows
        nextRowTokenized = nextRow.split(',')
       
        filtered = fnmatch.filter(nextRowTokenized[:2], Util.dateStampWildcard)
       
        if len(filtered) == 0:
            dataRows[iRow] = curRow+nextRow
            dataRows.remove(nextRow)
            iRow -= 2         
        
        iRow += 1

    # remove any empty rows
    for row in dataRows:
        if row.isspace():
            dataRows.remove(row)

    return dataRows

########################################################################
# Function that looks through row to make sure it contains only 5 elements
# if there are more than 5 there were commas in the title
#######################################################################
def SanitizeRow(row):
    cleanedRow = []

    nElements = len(row)

    if not nElements == 5:
        # merge elements together
        row[3 : nElements-1] = [''.join(row[3 : nElements-1])]

    cleanedRow = row

    return cleanedRow

########################################################################
# Function that takes a list of lists and turns them into a pandas
# data frame using the supplied column headings
#######################################################################
def CreatePandasDataFrame(listOfLists, listOfColumHeadings):
    df = pd.DataFrame(columns=listOfColumHeadings)    
    
    for i, aList in enumerate(listOfLists):
        if(len(aList) != len(listOfColumHeadings)):
            print('length mismatch! Skipping entry')
        else:
            df.loc[i] = aList

    return df            

########################################################################
# Function that takes in a CSV file, cleans it, and creates a pandas 
# data frame out of it
#######################################################################

def CSV2PandasDataFrame(inputFilePath, debugFlag = False):
    
    # Open the file for reading and store it as one big string
    inputFile = open(inputFilePath,'r')
    
    dataRows = inputFile.readlines()

    dataRows = SanitizeDataRows(dataRows)

    # break up the lines into tokens seperated by commas and store in a list of lists
    dataFrame = []
    for row in dataRows:
        tokenizedRow = row.split(',')
        cleanedRow = SanitizeRow(tokenizedRow)
        dataFrame.append(cleanedRow)

    if debugFlag:
        for row in dataFrame:
            Util.DisplayRow(row)
            if not len(row) == 6:
                input()
   
    if debugFlag:
        print('Creating Pandas DataFrme...')
    
    pandasDataFrame = CreatePandasDataFrame(dataFrame,['TimeStamp','URL', '# of Chars', 'Title', 'Article'])
    
    if debugFlag:
        print('DONE!')
    
    return pandasDataFrame


##########################################################################################################
# This function will turns every CSV file in a directory into a pandas data frame and then saves them as 
# a pickle file
##########################################################################################################
def PickleProductionRun(inputCSVFileDir, outputPickleFileDir):

    inputCSVFileDir = Util.CheckDirectoryPath(inputCSVFileDir)
    outputPickleFileDir = Util.CheckDirectoryPath(outputPickleFileDir)

    Util.CreateDirIfMissing(outputPickleFileDir)

    listOfFiles = Util.listdir_nohidden(inputCSVFileDir)
   
    print("Input Data(CSV): ", inputCSVFileDir)
    print("Output Data(PKL): ", outputPickleFileDir)
    print("# of Files: ", len(listOfFiles))
    
    for filename in listOfFiles:
        if Util.ExtensionOnly(filename) == 'csv':
            pdf = CSV2PandasDataFrame(inputCSVFileDir+filename)
            
            outputFilename = Util.FilenameOnly(filename)+".pkl"
            
            pdf.to_pickle(outputPickleFileDir + outputFilename)
        else:
            print('Invalid file type (only .csv files): ', filename)