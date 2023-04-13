# NewspaperSortByTicker
This is a python pipeline that sorts news articles based on the presence of stock ticker labels

The process has two stages. 

In the first stage the raw article data stored in CSV files is converted into a Panda's DataFrame object and 
then saved as a pickle file (.pkl). The articles text is cleaned and formated during this process. The same 
column names are used in the dataframe as the csv file. The process makes the following assumptions about the 
CSV columns and the file folder structure:

1. CSV columns = dateStamp, url, article length, title, article
2. file folder structure = {base_dir}/{year}/{month}/CSV/{filename}.csv (ex /home/nickshiell/storage/CC-NEWS-EN/2016/August/CSV/file-1.csv)

In the second stage the pickle files are loaded and each row is searched for stock tickers. A new column is added to the dataframe which is
labelled 'SEARCH_RESULTS'. The search results contain the symbol, company name, and index of where in the article the symbol was found.

The stock tickers need to be stored in a csv file with the coloums:

{stock symbol} , {company name}

for example: TNAV,TELENAV INC

# Stage 1: Pickling CSV files

The bash script autoPickleScript.sh can be used to automate the pickling process. In the bash script there are two array variables YEARS and MONTHS. 
The values in these arrays correspond to the years and months in the file folder structure mentioned above. 

Enter the correct years and months which need to be pickled.

The script takes two command line arguments as well 

1. The base folder of the CSV files (ex. /home/nickshiell/storage/CC-NEWS-EN). Which is the {base_dir} referenced above.
2. The location where the output (pickle files) should be saved too (ex. /home/nickshiell/storage/PickleJar)

The .pkl files will be store in a similar manner as the csv files (ie. {base_dir}/{year}/{month}/{pickleFile}.pkl

# Stage 2: Searching for Stock Symbols in the Pickle Files

The bash script autoStript.sh found in the Sorter/ directory can be used to automate search process. To use the script simply enter the correct 
information on lines 21 to 25. 

Line 21: YEARS = the years in the file folder structure (same as the pickling script)   

Line 22: MONTHS = the months in the file folder structure (same as the pickling script)   

Line 23: BASE_PKL_DATA_DIR = base directory  where ther pickle files were saved   

Line 24: TICKER_FILE_PATH = location of the file name tickersCompanyNames.csv"   

Line 25: NUM_PROCESSES = the number of processors to distribute the task over   

The results of the search are save to the same files that were used as input.   

# Viewing the results

