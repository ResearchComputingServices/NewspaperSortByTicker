#!/bin/bash
#####################################################################################################
# TEST RUN
# ./autoPickleScript.sh /home/nickshiell/storage/TestSet home/nickshiell/storage/TestSet/PickleJar
#
#YEARS=(2016)
#MONTHS=(August September October November December)
#####################################################################################################

#####################################################################################################
# PRODUCTION RUN
#./autoPickleScript.sh /home/nickshiell/storage/CC-NEWS-EN /home/nickshiell/storage/PickleJar
#
# For production run
# YEARS=(2016 2017 2018 2019 2020 2021 2022)
# MONTHS=(January February March April May June July August September October November December)
#####################################################################################################

#####################################################################################################
# EDIT THESE VALUES
YEARS=(2016 2017 2018 2019 2020 2021 2022)
MONTHS=(January February March April May June July August September October November December)
BASE_PKL_DATA_DIR="/home/nickshiell/storage/PickleJar"
TICKER_FILE_PATH="/home/nickshiell/NewspaperSTLSorting/TickerData/tickersCompanyNames.csv"
NUM_PROCESSES=10
#####################################################################################################

JOB_ARRAY=()

JOBS_COMPLETED=0
TOTAL_JOBS=0

# Create the jobs array
for year in ${YEARS[@]}; do
  for month in ${MONTHS[@]}; do
    JOB_ARRAY+=("${year}/${month}")
    ((TOTAL_JOBS=TOTAL_JOBS+1))
  done
done

NUMBER_OF_JOBS=${#JOB_ARRAY[@]}

# Assign the jobs in batchs, when a batch is complete move onto the next
while [ $JOBS_COMPLETED -lt $TOTAL_JOBS ]
do
  
  for (( i=0; i<$NUM_PROCESSES; i++ )); do
	  
    CUR_INPUT_DIR=${BASE_PKL_DATA_DIR}"/"${JOB_ARRAY[$JOBS_COMPLETED]}"/"
		  
    #echo python3 sorter.py ${CUR_INPUT_DIR} ${TICKER_FILE_PATH} &
    python3 sorter.py ${CUR_INPUT_DIR} ${TICKER_FILE_PATH} &
    
    pids[${i}]=$!
    ((JOBS_COMPLETED=JOBS_COMPLETED+1))

    # Break out if we run out of jobs
    if [ $JOBS_COMPLETED -ge $NUMBER_OF_JOBS ]
    then
      i=NUM_PROCESSES+1
    fi
  done
 
  # wait for all pids
  for pid in ${pids[*]}; do
    wait $pid
  done

  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
done