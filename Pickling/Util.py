import os
import operator
from pathlib import Path

########################################################################
# Common data
#######################################################################

dateStampWildcard = '20??-??-??T??:??:??Z'

monthList = [   'January', 'February', 'March', 'April', 
                'May', 'June', 'July', 'August', 
                'September', 'October', 'November', 'December'] 

# Location of the data set
dataLocationBase = ''

# This folder will contain files all the output
resultsOutputDirectory = ''

testText =  str('It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith' +
            ' his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly' +
            ' through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl' + 
            ' of gritty dust from entering along with him. The hallway smelt of boiled cabbage and old' +
            ' rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked' +
            ' to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man' + 
            ' of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston' + 
            ' made for the stairs. It was no use trying the lift. Even at the best of times it was seldom' +
            ' working, and at present the electric current was cut off during daylight hours. It was part' +
            ' of the economy drive in preparation for Hate Week. The flat was seven flights up, and' + 
            ' Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly,' + 
            ' resting several times on the way. On each landing, opposite the lift-shaft, the poster with' + 
            ' the enormous face gazed from the wall. It was one of those pictures which are so contrived' + 
            ' that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran.') 

testRepeatText = 'apple peach banana peach pear pineapple pear apple banana peach coconut peach pineapple peach apple pear apple peach pineapple'

testPositiveText = str('We spent an amazing long weekend at Nicolas’ home. The home is even better than in the pictures.' +
                    ' Communication with the host was excellent. There was self check in which was nice. The home is immaculate.' +
                    ' The furnishings are very tasteful, functional and comfortable. The kitchen is well stocked with anything' +
                    ' you could need to make a meal. The greatest part about this property is the scenery. The floor to ceiling' +
                    ' windows make you feel like you’re immersed in nature. There are well maintained beautiful grounds around you ' +
                    ' which lead to a lovely fire pit area and to the dock. We did go swimming off the dock and it was so much fun.' +
                    ' There are kayaks available as well. There’s a beautiful bird feeder which attracts gorgeous blue jays, squirrels' +
                    ' and chipmunks and we could have watched them all day. All in all you cannot go wrong with this air Bnb. 5 stars.' +
                    ' Would highly recommend!')

testNegativeText = str('Patricks cottage was nothing like I pictured it. The place was messy and had none of the necessary equipment you would' +
                    ' hope for. His communication with me was infrequent and curt. I struggled with the lock he didn\'t responded for two hours,' +
                    ' and also didn\'t help fix the problem. The environment and location were hard to find and I will never be coming back to this ' +
                    ' cottage in agin. I can hands down say this was the worst cottage to go that is close montreal.')
 
textAgainstCarbonTax =  str('According to a recent poll by a group called Canadians for Clean Prosperity, the Conservative Party should reconsider its opposition to carbon taxes. ' + 
                            'There is, indeed, a strong textbook case to be made for taxes on conventional pollution and carbon emissions—that if factories dirty the environment ' +
                            'by emitting smoke, factory owners should pay taxes to compensate society for the pollution. In theory, we can apply the same idea to carbon emissions, ' +
                            'which contribute to climate change. However, there are compelling reasons why Canadians should be very skeptical of carbon taxes. Famed economist ' +
                            'Milton Friedman, who the group cites as a possible supporter of carbon taxes, also noted that when government intervenes on environmental issues “it ' + 
                            'also is emitting smoke.” Like smoke from a factory’s chimney, imperfect government arrangements are a form of pollution because they impose costs on ' +
                            'third parties not involved in making those arrangements. As Friedman put it, “there’s a smokestack on the back of every government program.” ' +
                            'For carbon taxes, the smokestack is very large. The criteria that a carbon tax must meet to be sensible policy is considerably narrower than almost ' + 
                            'all carbon tax proponents will say, and in practise, carbon tax policies in Canada have deviated from these criteria, unnecessarily damaging the economy. ' +
                            'First, the tax rate must relate to the environmental harm of emissions or the “social cost of carbon,” which the Trudeau government assumes to be $50 ' +
                            'per tonne. But in fact, according to economic literature, the optimal carbon tax is actually much lower than the social cost. Because of how carbon ' +
                            'taxes compound the burden of existing taxes, the social cost should be discounted by the marginal cost of public funds (a measure of the economic cost ' +
                            'to the private sector of raising an additional dollar of government revenue). In the Canadian context, as economist Ross McKitrick has written, this ' +
                            'likely means discounting the social cost of carbon by about half. Then, as other economists note, the tax rate should be discounted again to account ' +
                            'for the fact that in some cases, the tax would not reduce emissions but simply cause emission-intensive activities to relocate, producing an economic ' +
                            'loss without any environmental benefit. Therefore, if the tax rate is instead targeted to reduce emissions by a certain amount—as in the Trudeau ' +
                            'government’s plan for a $170 per tonne to achieve the Paris agreement targets—then it’s contrary to the economic logic of how a carbon tax should work. ' +
                            'In addition, to mitigate the economic harm of a carbon tax, the revenues to government should be offset by equivalent cuts to other economically-harmful' + 
                            'taxes such as personal or corporate income taxes. Unfortunately, no current carbon tax policy in Canada looks like this. Lastly, the economic logic of ' +
                            'the carbon tax is to make emitters pay for the environmental harm they cause, eliminating the need for any other policies to reduce carbon emissions. ' +
                            'Indeed, the case for a carbon tax relies on the tax completely replacing—not being layered on top of—existing policies designed to reduce carbon emissions.' +
                            'Unless a proposed carbon tax meets these criteria, or at least comes very close, it should be rejected. Current carbon tax policies in Canada differ ' +
                            'materially from these criteria, and thus do more harm than good. They are, as Milton Friedman would say, like a giant smokestack.') 
 
 
textProCarbonTax =  str('Increasing the price of carbon is the most efficient and powerful method of combating global warming and reducing air pollution, ' +
                        'according to a new report from the International Monetary Fund. While the idea of carbon taxes on fossil fuel corporations has been ' +
                        'spreading across the globe in the past couple decades, increasing prices on carbon emissions has received widespread backlash from ' +
                        'those who argue the tax would raise energy bills. But economists have long contended that raising the cost of burning fossil fuels ' +
                        'like coal, oil and gas is the best way to mitigate climate change, and that revenue raised from the tax can be returned to consumers ' +
                        'through rebates and dividends. “We view fiscal policy as a crucial way of combating climate change,” said Paolo Mauro, deputy director ' +
                        'of Fiscal Affairs Department at the IMF. “You can reshape the tax system and you can reshape fiscal policy more generally in order to ' +
                        'discourage carbon emissions.” Global temperatures are projected to rise by roughly 4 C above preindustrial levels by 2100. The 2015 ' +
                        'Paris climate accord aims to limit warming to 2 C, with a long shot goal of 1.5 C. Most countries are not on track to achieve those ' +
                        'targets, and the U.S. plans to formally withdraw from the Paris agreement in 2020. More than 40 governments globally have implemented ' +
                        'a form of carbon pricing, whether it be through direct taxation on fossil fuel producers or cap-and-trade programs. However, the global ' +
                        'average carbon price is $2 a ton — a small fraction of the estimated $75 a ton price in 2030 consistent with a 2 C warming target, ' +
                        'according to the report. The IMF estimates a $75 a ton carbon tax will lead to the amount of emissions scientists estimate will ' +
                        'correspond to 2 C of warming. At that level, coal prices would rise by more than 200% above baseline levels in 2030. Under the same tax, ' + 
                        'the price of natural gas, which is used for power generation and for heating and cooking in households, would increase by 70% on average, ' + 
                        'with most of the impact in North and South America, where baseline prices are much lower. Gasoline prices would rise by 5% to 15% in most ' +
                        'countries. For electricity and gas, the price increases might seem substantial. However, those price rises are within the bounds of price ' +
                        'fluctuations experienced during the past few decades, according to the IMF. “If you think about it from a historical perspective, ' +
                        'gasoline prices fluctuate ... much more than that,” Mauro said. “Carbon taxes ... and similar arrangements to increase the price of ' +
                        'carbon, are the single most powerful and efficient tool to reduce domestic fossil fuel CO2 emissions,” the report said. Some countries ' +
                        'have prices on carbon In the U.S., a slew of presidential candidates have vowed to impose a carbon tax on corporations, proposals which ' +
                        'have come under attack from President Donald Trump and Republicans, who are repealing environmental regulations.Most carbon pricing efforts ' + 
                        'in the U.S. have occurred on the state level. Nine states in the Northeast participate in a cap-and-trade program that hands out carbon ' +
                        'pollution permits to power plants, and other states like New Jersey might join that system. Cap-and-trade programs work by taxing companies ' + 
                        'if they produce higher emissions than their permit allows. Companies that reduce emissions can sell unused permits to other firms. The ' +
                        'government also narrows the number of permits every year, reducing overall emissions. California has its own cap-and-trade program that ' +
                        'includes other polluters in addition to power plants. In Britain, coal use has gone down substantially after a carbon tax in 2013 prompted ' +
                        'electric utilities to switch away from coal. Canada has a carbon tax that started at $15 per ton of carbon dioxide this year and will rise ' +
                        'to $38 per ton by 2022. And China plans to start a cap-and-trade program beginning in 2020. “The cost of achieving emissions reductions ' +
                        'through these approaches would be lower than the costs to people and the planet from climate change,” the report said. “Finance ministers ' +
                        'in all countries are central to designing and implementing policies to meet emissions reductions in the most efficient, equitable, and ' +
                        'socially and politically acceptable way.”')

########################################################################
# Function that returns a list of all none hidden objects in directory
#######################################################################

def listdir_nohidden(directory):

    listOfContents= []

    if os.path.exists(directory):

        listOfContents = os.listdir(directory)

        for item in listOfContents:
            if item.startswith('.'):
                listOfContents.remove(item)

    return listOfContents

########################################################################
# Function that creates the directory if it does not exist
#######################################################################

def CreateDirIfMissing(directory):

    Path(directory).mkdir(parents=True, exist_ok=True)

########################################################################
# These functions returns just the filename without the extension or vice versa
#######################################################################
def FilenameOnly(filenameWithExtension):
    return filenameWithExtension.split('.')[0]

def ExtensionOnly(filenameWithExtension):
    return filenameWithExtension.split('.')[1]

########################################################################
# This function makes sure the directory path ends with a '/'
#######################################################################
def CheckDirectoryPath(dirPath):

    if dirPath[-1] != '/':
        dirPath += '/'

    return dirPath

########################################################################
# Function that returns a months number equivalent
#######################################################################

def MonthWordToNumber(monthWord):

    monthNumber = '-1'

    counter = 1
    for m in monthList:
        if m.lower() == monthWord.lower():
            monthNumber = str(counter)
            break
        else:
            counter += 1

    return monthNumber 

########################################################################
# Function that nicely displays a data row as a column
#######################################################################

def DisplayRow(row, maxLength = 750):
    print(len(row))

    for item in row:
        if len(item) < maxLength:
            print(item.strip(), '\t ***')
        else:
            print('ARTICLE\t ***')

########################################################################
# Function that nicely displays a sorted dictionary
#######################################################################
def DisplaySortedDict(aDict, nDisplay = 1000, reverse = True):
    sortedDict = sorted(aDict.items(), key=operator.itemgetter(1))
    
    if reverse:
        sortedDict.reverse()
    
    counter = 0
    for pair in sortedDict:
        print(pair[0], ' :  ', pair[1])

        if counter < nDisplay:
            counter += 1
        else:
            break

########################################################################
# Function that prints a sorted dictionary to the file name pass to it
#######################################################################
def ReportSortedDict(outputFileName, aDict, nDisplay = 1000, reverse = True):
  
    outputFile = open(outputFileName,'a+')
    
    sortedDict = sorted(aDict.items(), key=operator.itemgetter(1))
    
    if reverse:
        sortedDict.reverse()
    
    counter = 0
    for pair in sortedDict:
        outputFile.write(str(pair[0])+ ' :  '+ str(pair[1])+'\n')

        if counter < nDisplay:
            counter += 1
        else:
            break

    outputFile.close()

######################################################
# This function counts how many foriegn articles are
# contained in the list and keeps track of where they
# are from (ex. .de .jp .co.uk)
######################################################
def ReportForiegnTLDs(dictToIgnore,outputFileName):
    
    outputFile = open(outputFileName,'a+')

    dictOfForiegnTLDs = {}
    value = 0

    for key in dictToIgnore:
        
        tokenKey = key.split('.')

        curTLD = tokenKey[-1].strip()

        if not curTLD in keepTLDList:
            value += dictToIgnore[key]

            if not curTLD in dictOfForiegnTLDs:
                dictOfForiegnTLDs[curTLD] = dictToIgnore[key]
            else:
                dictOfForiegnTLDs[curTLD] += dictToIgnore[key]
    
    outputFile.write('# of Foriegn Articles: ' + str(value) + '\n')


    for tld in dictOfForiegnTLDs:
        outputFile.write(tld+ ' : '+ str(dictOfForiegnTLDs[tld])+'\n')

    outputFile.close()

########################################################################
# Function that nicely displays a dictionary
#######################################################################
def DisplayDict(aDict, nDisplay = 10000000):
    counter = 0
    for key in aDict:
        print(key, ' :  ', aDict[key])

        if counter < nDisplay:
            counter += 1
        else:
            break

########################################################################
# Splits the data frame in two parts [UID,Article] & [UID, the rest]
#######################################################################
def SplitDataFrame(fullDataFrame):
    metaDataList = []
    articleDictionary = {}

    for item in fullDataFrame:
        date = item[0]
        fullURL = item[1]
        length = item[2]
        title = item[3]
        article = item[4]
        UID = item[5]
        baseURL = item[6]

        articleDictionary[UID] = article

        metaDataList.append([date,fullURL,length,title,UID,baseURL])

    return metaDataList, articleDictionary

######################################################
# writes the data to a sorted folder structure...
# /state/year/month/FILES
######################################################
def HandleMultiStateEntries(metaDataList):
    
    newMetaDataList = []

    for row in metaDataList:
        # the assigned state is the last entry in the row
        stateEntry = row[-1]

        stateEntrySplit = stateEntry.split(',')

        # if there is more than one state listed need to make a seperate line
        if len(stateEntrySplit) > 1:           
            for state in stateEntrySplit:
                newRow = row
                newRow[-1] = state
                newMetaDataList.append(newRow.copy())

        else:
            newMetaDataList.append(row)

    return newMetaDataList
    
######################################################
# writes the data to a sorted folder structure...
# /state/year/month/FILES
######################################################
def SaveSortedArticles(year,month,metaDataList,articleDictionary):  

    # sort the metaDataList by the state name (last column)
    metaDataList.sort(key=lambda x: x[-1])    

    sortedDataDirectory = resultsOutputDirectory + 'States'

    # create an file object
    outputFile = open(sortedDataDirectory+'/empty.dat','w+')
    outputFile.close()

    nRows = len(metaDataList)
    iRow = 0
    while iRow < nRows:
        curRow = metaDataList[iRow]
        currentStateName = curRow[-1]

        # open the file if it has been closed
        if outputFile.closed:
            outputFileLocation = sortedDataDirectory + '/' + currentStateName + '/' + year + '/' + month + '/'
            
            # create the folder if it doesnt exist
            Path(outputFileLocation).mkdir(parents=True, exist_ok=True)

            outputFilename = currentStateName + '_' + year + '_' + month + '.csv'
            outputFile = open(outputFileLocation + outputFilename, 'a+')

        # write what we want to the file
        date = curRow[0].strip()
        fullURL = curRow[1].strip()
        length = curRow[2].strip()
        title = curRow[3].strip()
        UID = curRow[4].strip()
        article = articleDictionary[UID].strip()
        outputStr = date+','+fullURL+','+length+','+title+','+article+'\n'
        outputFile.write(outputStr)              
        
        # check if the next row has the same state name as the current one
        # if not close the file
        if iRow+1 < nRows:
            nextRow = metaDataList[iRow+1]
            if not nextRow[-1] == curRow[-1]:
                outputFile.close()
        else:
            outputFile.close()

        iRow += 1

######################################################
# this function saves the results to a file
######################################################

def SaveResultsToFile(dataFrame, maxLength = 750):
    print('Writing to file...')

    # sort the dataFrame by the state name (last column)
    dataFrame.sort(key=lambda x: x[-1])    

    outputFile = open(resultsOutputDirectory+'empty.dat','w+')
    outputFile.close()

    nRows = len(dataFrame)
    iRow = 0
    while iRow < nRows-1:
        curRow = dataFrame[iRow]
        nextRow = dataFrame[iRow+1]

        # open the file if it has been closed
        if outputFile.closed:
            outputFilename = curRow[-1]+'.csv'
            outputFile = open(resultsOutputDirectory + outputFilename, 'a+')

        # write what we want to the file
        outputStr = ''
        rowLength = len(curRow)
        itemCounter = 0
        while itemCounter < rowLength-1:
            item = curRow[itemCounter]
            if len(item) < maxLength:
                outputStr += item.strip() + ','
            itemCounter += 1
            
        outputFile.write(outputStr[:-1]+'\n')

        if not nextRow[-1] == curRow[-1]:
            outputFile.close()

        iRow += 1


#########################################################
# Add a URL to the dictionary:
# we need to check if the URL already exists and if it 
# does we need to append to the value instead of just
# overwriting it
#########################################################

def AddURL2Dict(dict,url,state):

    # Construct the appropriate alternate URL    
    alternateURL = ''
    if not 'www.' in url:
        # add www to URL
        alternateURL = 'www.'+url
    else:
        # remove www from URL
        alternateURL = url[4:]

    if url in dict:
        if not state in dict[url]:
            dict[url] = dict[url] + ',' + state
    else:
        dict[url] = state

    if alternateURL in dict:
        if not state in dict[alternateURL]:
            dict[alternateURL] = dict[alternateURL] + ',' + state
    else:
        dict[alternateURL] = state
    
    return dict


#########################################################
# Load all the state sorted newspapers into a dictionary
# key = paperURL
# value = state
#########################################################

def GetDictionaryOfStatePapers():
    statePaperFiles = os.listdir(statePaperFilesLocation)

    dictionaryOfStatePapers = {}

    for filename in statePaperFiles:

         # the value in the dictionary is the stateName
        value = filename.split('.')[0]
        
        with open(statePaperFilesLocation + filename,'r') as openfileobject:
            for line in openfileobject:
                pair = line.split(',')
                if len(pair) == 2:
                    if not pair[1].strip() in ignoreList:

                        # Clean up the URL
                        url = pair[1].strip()
                        if 'http://' in url:
                            url = url[7:]
                        if 'https://' in url:
                            url = url[8:]
                        if url[-1] == '/':
                            url = url[:-1]
     
                        dictionaryOfStatePapers = AddURL2Dict(dictionaryOfStatePapers, url, value)

    return dictionaryOfStatePapers

######################################################
# this function updates the results stats
######################################################
def UpdateResults(state, dictResults):

    stateSplit = state.split(',')

    if len(stateSplit) == 1:
        if state in dictResults:
            dictResults[state] += 1
        else:
            dictResults[state] = 1
    else:
        for state in stateSplit:
            if state in dictResults:
                dictResults[state] += 1
            else:
                dictResults[state] = 1
