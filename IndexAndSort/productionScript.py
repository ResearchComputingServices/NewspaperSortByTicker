import sys
import time

from ArticleIndexer import ArticleIndexerProductionRun
from TickerSorter import TickerSorterProductionRun
import Util

#/home/nickshiell/storage/TestSet

inputPKLDir = ''
outputPKLDir = ''
tickerListFilePath = ''

# Make sure that the command line args are present
if len(sys.argv) == 4:
    inputPKLDir = sys.argv[1]
    outputPKLDir = sys.argv[2]
    tickerListFilePath = sys.argv[3]
else:
    print('ERROR: invalid command line args: ', sys.argv)
    exit(0)

startTime = time.time()

#ArticleIndexerProductionRun(inputPKLDir,outputPKLDir)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
TickerSorterProductionRun(inputPKLDir,outputPKLDir,tickerListFilePath)

executionTime = (time.time() - startTime)
print('Execution time for ', inputPKLDir,': ' + str(executionTime),'[s]')
print('=================================================================================================')