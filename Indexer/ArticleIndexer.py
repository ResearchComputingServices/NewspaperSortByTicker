import pandas as pd
import os
import sys
import time

from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

import Util

##########################################################################################################
# This function removes punctuation from the text
##########################################################################################################
def RemovePunctuation(text):
    cleanedText = ''
    for word in word_tokenize(text):
        
        if word.isalpha():
            cleanedText += word + ' '            
   
    return cleanedText 

##########################################################################################################
# This function lemmatizes the text passed to it:
##########################################################################################################
def LemmatizeText(text):
    lemmatizedText = ''
    lemmatizer = WordNetLemmatizer()
    for word in word_tokenize(text):
        lemmatizedText += lemmatizer.lemmatize(word) + ' '
   
    return lemmatizedText


##########################################################################################################
# This function remove stop words and if caseFlag is true puts everything in lowercase.
##########################################################################################################
def RemoveStopWords(text, caseFlag = True):  
    swList = stopwords.words('english')

    cleanedText = ''
    for word in word_tokenize(text):
        if word.lower() not in swList and word.isalpha():
            addWord = word
            
            if caseFlag:
                addWord = addWord.lower()
            
            cleanedText += addWord + ' '
    
    return cleanedText

##########################################################################################################
# This function creates a dictionary (word : frequency) from the text that provided. The text
# is split using the supplied delim
##########################################################################################################
def TextIndexer(text, delim = ' '):
    listOfWords = text.split(delim)
       
    textIndex = {}
    
    for word in listOfWords:
        
        if not word.isalpha():
            continue
        
        if word not in textIndex.keys():
            textIndex[word] = 1
        else:
            textIndex[word] = textIndex[word]+1
             
    return textIndex

##########################################################################################################
# This function cleans and index the pandas data frame which is passed to it
########################################################################################################## 
def CleanAndIndexPandasDF(  pdf, 
                            DEBUG = False, 
                            doStopWords = False,
                            doPunctuation = True,
                            doLemma = False):
                            
    # Add a column to the data frame to hold the text index
    if 'TextIndex' in pdf.columns:
        pdf.drop(['TextIndex'], axis=1)

    pdf['TextIndex'] = ""

    # Go through the data frame row by row clean up the aritlce index it
    for iRow, row in pdf.iterrows():
        articleText = str(row['Article'])
        cleanedArticleText = articleText

        #cleanedArticleText = Util.ExtractArticle(cleanedArticleText,True)

        if DEBUG:
            print('ORIGINAL TEXT:')
            print(articleText)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        if doStopWords:      
            cleanedArticleText = RemoveStopWords(cleanedArticleText)
            
            if DEBUG:
                print('STOP WORDS REMOVED:')
                print(cleanedArticleText)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        if doPunctuation:
            cleanedArticleText = RemovePunctuation(cleanedArticleText)
            
            if DEBUG:
                print('PUNCTUATIO REMOVED:')
                print(cleanedArticleText)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        if doLemma:
            cleanedArticleText = LemmatizeText(cleanedArticleText)

            if DEBUG:
                print('LEMMATIZED:')
                print(cleanedArticleText)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        # Create index and add it to the data frame 
        textIndexDict = TextIndexer(cleanedArticleText)
        pdf.loc[iRow]['TextIndex'] = textIndexDict

        if DEBUG:
            print('INDEXED TEXT:')
            print(textIndexDict)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            input()

            if iRow % 100 == 0:
                print(iRow, ' / ', len(pdf.index))
    
    return pdf

##########################################################################################################
# This function cleans and index the pickle file which is passed to it
########################################################################################################## 
def CleanAndIndexPickleFile(inputPickleFilePath, 
                            DEBUG = False, 
                            doStopWords = False,
                            doPunctuation = True,
                            doLemma = False):

    pdf = pd.read_pickle(inputPickleFilePath)

    return CleanAndIndexPandasDF(pdf, DEBUG, doStopWords, doPunctuation, doLemma)

##########################################################################################################
# This function Cleans, Indexs, as Saves a single PKL file
##########################################################################################################
def CleanAndIndexSinglePKLFile(filename, inputPickleFileDir, outputPickleFileDir):

    # make sure the directories have the right format (ie. end with /
    inputPickleFileDir = Util.CheckDirectoryPath(inputPickleFileDir)
    outputPickleFileDir = Util.CheckDirectoryPath(outputPickleFileDir)

    pdf = pd.DataFrame()

    # Check the correct type of file has been passed in
    if Util.ExtensionOnly(filename) != 'pkl':
         print('Invalid file type (only .pkl files): ', filename)
    else:
        # Open and clean the file
        inputPickleFilePath = inputPickleFileDir + filename    
        pdf = CleanAndIndexPickleFile(inputPickleFilePath)
        
        # Now that The data file has been cleaned and index save the PKL file
        outputFilePath = outputPickleFileDir + filename
        pdf.to_pickle(outputFilePath)
    
    return pdf

##########################################################################################################
# This function Cleans and Indexs all the Pickle files in a given directory
##########################################################################################################
def ArticleIndexerProductionRun(inputPickleFileDir, outputPickleFileDir):

    inputPickleFileDir = Util.CheckDirectoryPath(inputPickleFileDir)
    outputPickleFileDir = Util.CheckDirectoryPath(outputPickleFileDir)

    listOfFiles = Util.listdir_nohidden(inputPickleFileDir)

    print("INDEXING FILES:")
    print("Input Data: ", inputPickleFileDir)
    print("Output Data: ", outputPickleFileDir)
    print("# of Files: ", len(listOfFiles))

    for filename in listOfFiles:
        CleanAndIndexSinglePKLFile(filename,inputPickleFileDir, outputPickleFileDir)

      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
#def TextIndexer(text, delim = ' '):
#    listOfWords = text.split(delim)
#    
#    listOfWords.sort()
#    
#    textIndex = {}
#    
#    nWords = len(listOfWords)
#    iWord = 0
#    while iWord < nWords:
#        
#        curWord = listOfWords[iWord]
#        counter = 1
#        
#        if(iWord+counter >= nWords):
#            break
#        
#        while listOfWords[iWord+counter] == curWord:
#            counter += 1
#            if(iWord+counter >= nWords):
#                break
#        
#        textIndex[curWord] = counter
#        
#        iWord += counter
#          
#    return textIndex