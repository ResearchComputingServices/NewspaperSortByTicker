import Picklizer
import sys
import Util
import time

#/home/nickshiell/storage/TestSet

inputCSVDir = ''
outputPKLDir = ''

# Make sure that the command line args are present
if len(sys.argv) == 3:
    inputCSVDir = sys.argv[1]
    outputPKLDir = sys.argv[2]
else:
    print('ERROR: invalid command line args: ', sys.argv)
    exit(0)

startTime = time.time()
Picklizer.PickleProductionRun(inputCSVDir,outputPKLDir)
executionTime = (time.time() - startTime)
print('Execution time for ', inputCSVDir,': ' + str(executionTime),'[s]')