import pandas as pd
import os

from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

##########################################################################################################
# These function perform a lexicon-based Sentiment Analysis of an index text corpus
##########################################################################################################

def CalculateOccurrences(textIndexDict, wordList):
    val = 0
    
    for word in wordList:
        if word in textIndexDict:
            val += textIndexDict[word]
            
    return val
    
def CalculateSentimentIndex(textIndexDict):
    posWordList = opinion_lexicon.positive()
    negWordList = opinion_lexicon.negative()
   
    sIndex = 0
   
    length = len(textIndexDict)
   
    if length > 0:
        pos = CalculateOccurrences(textIndexDict, posWordList)
        neg = CalculateOccurrences(textIndexDict, negWordList)    
        sIndex =  (pos - neg) / length
    
    return sIndex

##########################################################################################################
# This function takes in a pandas data from with the following columns:
# 'TimeStamp','URL', '# of Chars', 'Title', 'Article', 'TextIndex'
# it appends a column "S_Index" to the dataframe, it then calculates a Sentiment Index for each row
# and saves the value in the newly appended column. Finally, it then returns the data frame
##########################################################################################################

def SentimentAnalyzer(pandasDataFrame):

    # Appended new column
    pandasDataFrame['S_Index'] = ""

    #TODO: Check to make sure the pdf have the correct columns
    for iRow, row in pandasDataFrame.iterrows():
        textIndex = row['TextIndex']
        
        # calculate the sIndex for the current row
        sIndex = CalculateSentimentIndex(textIndex)
        
        # and then store the index value in the appropriate column
        pandasDataFrame.loc[iRow]['S_Index'] = sIndex
         
    # retrun the updated pandas data frame
    return pandasDataFrame
    