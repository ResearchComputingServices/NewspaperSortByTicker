import pandas as pd
import os

from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

import Util
from ArticleSorter.Picklizer import *

# Location of the data set
Util.dataLocationBase = '/home/nickshiell/storage/TestSet/'
    
##########################################################################################################
# This function creates a dictionary (word : frequency) from the text that provided based on the delim
##########################################################################################################
def TextIndexer(text, delim = ' '):
    listOfWords = text.split(delim)
    
    listOfWords.sort()
    
    textIndex = {}
    
    nWords = len(listOfWords)
    iWord = 0
    while iWord < nWords:
        
        curWord = listOfWords[iWord]
        counter = 1
        
        if(iWord+counter >= nWords):
            break
        
        while listOfWords[iWord+counter] == curWord:
            counter += 1
            if(iWord+counter >= nWords):
                break
        
        textIndex[curWord] = counter
        
        iWord += counter
          
    return textIndex
     
##########################################################################################################
# This is where the main code starts
##########################################################################################################
year = '2016'
month = 'Madeupember'

currentDirectory = Util.dataLocationBase+year+'/'+month+'/CSV/'
listOfFiles = Util.listdir_nohidden(currentDirectory)

swList = stopwords.words('english')


for filename in listOfFiles:

    inputFileLocation = currentDirectory + filename   
    inputFile = open(inputFileLocation,'r')
    
    df = GetDataFrame(year, month, filename)
    
    for index, row in df.iterrows():
        #articleText = str(row['Article'])
        articleText = Util.testPositiveText
        cleanedArticleText = ''
        
        # remove stop words/punctuation and put everything in lowercase.
        # - swlist is a list of stop words in english from NLTK
        # - isaplha() tests if a string contains only alphabeta symbols
        # nb. word_tokenize() seperates words from puncuation
        for word in word_tokenize(articleText.lower()):
            if word not in swList:
                cleanedArticleText += word + ' '
                
        newStr = ''
        for word in word_tokenize(cleanedArticleText.lower()):
            if word.isalpha():
               newStr += word + ' ' 
        cleanedArticleText = newStr
        
        # lemmatize words
        newStr = ''
        lemmatizer = WordNetLemmatizer()
        for word in word_tokenize(cleanedArticleText):
            newStr += lemmatizer.lemmatize(word) + ' '
        cleanedArticleText = newStr
        
        # create a dictionary (word : frequency) from the cleaned text that 
        textIndexDict = TextIndexer(cleanedArticleText)
            
   
        sIndex = CalculateSentimentIndex(textIndexDict,positiveWordsList,negativeWordsList)
        
        print("sIndex = ", sIndex)
        
        exit()
        
        
   