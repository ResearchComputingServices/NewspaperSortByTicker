#!/bin/bash
# TEST RUN
# ./autoSortScript.sh /home/nickshiell/storage/TestSet/PickleJar home/nickshiell/storage/TestSet/PickleJar

JOB_ARRAY=()

NUM_PROCESSES=10
JOBS_COMPLETED=0
TOTAL_JOBS=0

# Check that exactly one command line argument has been passed
if [ "$#" -ne 2 ]; then
  echo "Please provide an INPUT and OUTPUT directory"
  exit
fi

# assign the input and output directories
BASE_INPUT_PKL_DATA_DIR=$1
BASE_OUTPUT_PKL_DATA_DIR=$2

# Create the jobs array
FILES=`ls ${BASE_INPUT_PKL_DATA_DIR}/*.pkl`
for entry in ${FILES}
do
	base_name=$(basename ${entry})
	JOB_ARRAY+=("$base_name")
	((TOTAL_JOBS=TOTAL_JOBS+1))
done

NUMBER_OF_JOBS=${#JOB_ARRAY[@]}

# Assign the jobs in batchs, when a batch is complete move onto the next
while [ $JOBS_COMPLETED -lt $TOTAL_JOBS ]
do
  
	for (( i=0; i<$NUM_PROCESSES; i++ )); do
	  
		FILENAME=${JOB_ARRAY[$JOBS_COMPLETED]}
		#echo python3 sfProductionScript.py ${FILENAME} ${BASE_INPUT_PKL_DATA_DIR} ${BASE_OUTPUT_PKL_DATA_DIR} &
		python3 sfProductionScript.py ${FILENAME} ${BASE_INPUT_PKL_DATA_DIR} ${BASE_OUTPUT_PKL_DATA_DIR} &
			    
		pids[${i}]=$!
		((JOBS_COMPLETED=JOBS_COMPLETED+1))

		# Break out if we run out of jobs
		if [ $JOBS_COMPLETED -ge $NUMBER_OF_JOBS ]
		then
			i=NUM_PROCESSES+1
		fi
  	done
 
	#wait for all pids
	for pid in ${pids[*]}; do
		wait $pid
	done

	echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
done