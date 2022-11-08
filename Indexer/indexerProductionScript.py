import sys
import time

from ArticleIndexer import ArticleIndexerProductionRun

inputPKLDir = ''
outputPKLDir = ''

# Make sure that the command line args are present
if len(sys.argv) == 3:
    inputPKLDir = sys.argv[1]
    outputPKLDir = sys.argv[2]
else:
    print('ERROR: invalid command line args: ', sys.argv)
    exit(0)

startTime = time.time()

ArticleIndexerProductionRun(inputPKLDir,outputPKLDir)

executionTime = (time.time() - startTime)
print('Execution time for ', inputPKLDir,': ' + str(executionTime),'[s]')