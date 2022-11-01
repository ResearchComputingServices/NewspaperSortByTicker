import pandas as pd

#pickleFilePath = '/home/nickshiell/storage/TestSet/PickleJar/2016/August/file-1.pkl'
pickleFilePath = '/home/nickshiell/storage/TestSet/TestPickle/Test.pkl'

pdf = pd.read_pickle(pickleFilePath)

for iRow, row in pdf.iterrows():

    title = row['Title']
    tickers = row['Ticker(s)']
    index = row['TextIndex']
    article = row['Article']

    listOfKeys = list(index.keys())
    listOfKeys.sort()

    print(article)    
    print(listOfKeys)
    print(title,': ', tickers)

    input()