import pandas as pd
import sys
import time

from ArticleIndexer import CleanAndIndexPandasDF
from TickerSorter import TickerSorterPandasDF
import Util

#/home/nickshiell/storage/TestSet/TestPickle/Test.pkl

inputPKLDir = ''
outputPKLDir = ''
tickerListFilePath = '../TickerData/tickersCompanyNames.csv'

# Make sure that the command line args are present
if len(sys.argv) == 4:
    filename = sys.argv[1]
    inputPKLDir = sys.argv[2]
    outputPKLDir = sys.argv[3]
else:
    print('ERROR: invalid command line args: ', sys.argv)
    exit(0)

# Make sure the provided directories end with /
inputPKLDir = Util.CheckDirectoryPath(inputPKLDir)
outputPKLDir = Util.CheckDirectoryPath(outputPKLDir)

startTime = time.time()
print('Processing file: ', filename)
print('From: ', inputPKLDir)
print('Save to: ', outputPKLDir)
print('')
# open the pickle file
print('Reading file...',end='',flush=True)
inputPickleFilePath = inputPKLDir + filename 
pdf = pd.read_pickle(inputPickleFilePath)
print('DONE!')

# do the analysis
print('Cleaning and indexing...',end='',flush=True)
pdf = CleanAndIndexPandasDF(pdf)
print('DONE!')

print('Sorting...',end='',flush=True)
pdf = TickerSorterPandasDF(pdf,tickerListFilePath)
print('DONE!')

# Now that The data file has been cleaned and index save the PKL file
outputFilePath = outputPKLDir + filename
pdf.to_pickle(outputFilePath)

executionTime = (time.time() - startTime)
print('Total execution time for ', filename,': ' + str(executionTime),'[s]')
print('=================================================================================================')