import pandas as pd
import os
import sys
import Util

from Picklizer import CSV2PandasDataFrame
from ArticleIndexer import CleanAndIndexPickleFile, CleanAndIndexPandasDF
from TickerSorter import ReadTickers, SearchForTickersInPDF, SearchForTickersInPickleFile

inputCSVFilePath = '/home/nickshiell/storage/TestSet/2016/Madeupember/CSV/Test.csv'
inputPickleFilePath = '/home/nickshiell/storage/TestSet/TestPickle/Test.pkl'
outputPickleFilePath = '/home/nickshiell/storage/TestSet/TestPickle/'
tickerLabelsFilePath = './stockTickerLabels.dat'

# Make sure that the command line args are present
#if len(sys.argv) == 4:
#    inputPickleFilePath =  sys.argv[1]
#    outputPickleFilePath = sys.argv[2]
#    tickerLabelsFilePath = sys.argv[3]
#else:
#    print('ERROR: invalid command line args: ', sys.argv)
#    exit()
    
#tickerList = ReadTickers(tickerLabelsFilePath)
#pdf = CSV2PandasDataFrame(inputCSVFilePath)
#pdf = CleanAndIndexPandasDF(pdf,False,False,True,True)
#pdf = SearchForTickersInPDF(pdf,tickerList,True)



