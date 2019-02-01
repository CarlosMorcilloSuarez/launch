#!/bin/bash


run_tests(){

# Tests are written here ###################################

# Test ----------------------------------------
initialize_test 'CNAG: Works with basic configuration'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
    --file-only \
    --name zdog1qc \
    --output-directory ./test/outputs \
    -c "fastqc -i ./dog1.fastq -o ./dog1" \

compare_files \
  ./test/outputs/zdog1qc.cmd \
  ./test/inputs/references/test1.cmd


# Test ----------------------------------------
initialize_test 'CNAG: Includes Time Limit and Modules'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
  --file-only \
  --name unzip003 \
  --limit 05:00:00 \
  --modules "GZIP SRA" \
  --output-directory ./test/outputs \
  -c "gzip -d bigfile.fastq"

compare_files \
  ./test/outputs/unzip003.cmd \
  ./test/inputs/references/test2.cmd


# Test ----------------------------------------
initialize_test 'CNAG: Includes Tasks and CPUs per Task'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
  --file-only \
  --name tasks_and_cpus \
  --tasks 2*3 \
  --output-directory ./test/outputs \
  -c "ls -ald *"

compare_files \
  ./test/outputs/tasks_and_cpus.cmd \
  ./test/inputs/references/test3.cmd


# Test ----------------------------------------
initialize_test 'CNAG: Assigns long jobs to Low Priority Queue'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
  --file-only \
  --name low_priority_queue \
  --limit 35:00:00 \
  --output-directory ./test/outputs \
  -c "ls -ald *"

compare_files \
  ./test/outputs/low_priority_queue.cmd \
  ./test/inputs/references/test4.cmd


# Test ----------------------------------------
initialize_test 'CNAG: Shows Version with --version/-v'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
STRING=$(./launch --version)
STRING2=$(./launch -v)
REFERENCE_STRING='launch Version: '$(cat launch.py |
                  grep __version__ |
                  head -1 |
                  cut -d'"' -f2)

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"
compare_strings \
  "${STRING2}" \
  "${REFERENCE_STRING}"


# Test ----------------------------------------
initialize_test 'CNAG: launches a job'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(\
    ./launch \
      --name launchesJob \
      --output-directory ./test/outputs \
      -c "ls -ald *" \
    | tail -n +2
    )
PATH=${OLD_PATH}
REFERENCE_STRING="mnsubmit ./test/outputs/launchesJob.cmd"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"


# Test ----------------------------------------
initialize_test 'CNAG: launches a job dependent on another'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(\
    ./launch \
      --name dependentJob \
      --dependent-on 666845:333444 \
      --output-directory ./test/outputs \
      -c "gzip -d bigfile.fastq" \
    | tail -n +2
    )
PATH=${OLD_PATH}
REFERENCE_STRING="mnsubmit -dep afterok:666845:333444 ./test/outputs/dependentJob.cmd"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"

# Test ----------------------------------------
initialize_test 'Simplifies blank spaces in command'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
COMMAND=" 
          ls -alh *.txt
          mv \
          veryLongFile.txt \
          veryVeryLongFile.txt \
        "

./launch \
  --file-only \
  --name simplifiedSpaces \
  --limit 1:00:00 \
  --output-directory ./test/outputs \
  -c "$COMMAND"

compare_files \
  ./test/outputs/simplifiedSpaces.cmd \
  ./test/inputs/references/test5.cmd    
  
# Test ----------------------------------------
initialize_test 'CNAG: Returns id after launching job'

cp ./test/inputs/launchConfig_CNAG.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(./launch \
          --name returnsID \
          --output-directory ./test/outputs \
          -c "gzip -d bigfile.fastq" \
        | head -1)

PATH=${OLD_PATH}
REFERENCE_STRING="15565827 Submitted batch job 15565827"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"
  
# Test ----------------------------------------
initialize_test 'UPF: Works with basic configuration'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
    --file-only \
    --name upfBasic \
    --output-directory ./test/outputs \
    -c "ls -al" \

compare_files \
  ./test/outputs/upfBasic.cmd \
  ./test/inputs/references/test6.cmd

  
# Test ----------------------------------------
initialize_test 'UPF: Includes Time Limit and Modules'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
  --file-only \
  --name timeModulesUPF \
  --limit 05:00:00 \
  --modules "GZIP SRA" \
  --output-directory ./test/outputs \
  -c "gzip -d bigfile.fastq"

compare_files \
  ./test/outputs/timeModulesUPF.cmd \
  ./test/inputs/references/test7.cmd
  
# Test ----------------------------------------
initialize_test 'UPF: Includes Tasks and CPUs per Task'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
./launch \
  --file-only \
  --name UPF_tasks_cpus \
  --tasks 2*3 \
  --output-directory ./test/outputs \
  -c "ls -ald *"

compare_files \
  ./test/outputs/UPF_tasks_cpus.cmd \
  ./test/inputs/references/test8.cmd  
  
# Test ----------------------------------------
initialize_test 'UPF: Shows Version with --version/-v'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
STRING=$(./launch --version)
STRING2=$(./launch -v)
REFERENCE_STRING='launch Version: '$(cat launch.py |
                  grep __version__ |
                  head -1 |
                  cut -d'"' -f2)

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"
compare_strings \
  "${STRING2}" \
  "${REFERENCE_STRING}"


# Test ----------------------------------------
initialize_test 'UPF: launches a job'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(\
    ./launch \
      --name UPFlaunchesJob \
      --output-directory ./test/outputs \
      -c "ls -ald *" \
    | tail -n +2
    )
PATH=${OLD_PATH}
REFERENCE_STRING="sbatch ./test/outputs/UPFlaunchesJob.cmd"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"
  
  
# Test ----------------------------------------
initialize_test 'UPF: launches a job dependent on another'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(\
    ./launch \
      --name UPFdependentJob \
      --dependent-on 666845:333444 \
      --output-directory ./test/outputs \
      -c "gzip -d bigfile.fastq" \
    | tail -n +2
    )
PATH=${OLD_PATH}
REFERENCE_STRING="sbatch --dependency afterok:666845:333444 ./test/outputs/UPFdependentJob.cmd"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"


# Test ----------------------------------------
initialize_test 'UPF: Returns id after launching job'

cp ./test/inputs/launchConfig_UPF.py ./launchConfig.py
rm ./launchConfig.pyc
OLD_PATH=${PATH}
PATH=.:${OLD_PATH}
STRING=$(./launch \
          --name UPFreturnsID \
          --output-directory ./test/outputs \
          -c "gzip -d bigfile.fastq" \
        | head -1)

PATH=${OLD_PATH}
REFERENCE_STRING="15565827 Submitted batch job 15565827"

compare_strings \
  "${STRING}" \
  "${REFERENCE_STRING}"
  
############################################################
}


# Testing Functions

initialize_test(){
  echo
  echo $1
}


compare_strings(){
  STRING=$1
  REFERENCE_STRING=$2

  if [ "${STRING}" = "${REFERENCE_STRING}" ]
  then
    echo "------------------------------------------------- OK"
  else
    echo "ERROR ------------------------------ ERROR"
    echo ${STRING}---${REFERENCE_STRING}--- Seem to be different
  fi
}


compare_files(){
  FILE_NAME=$1
  MODEL_FILE=$2

  # Checks expected outputfile
  if [ -f "${FILE_NAME}" ]
  then
      zdiff ${FILE_NAME} ${MODEL_FILE} > /dev/null
      if test $? -eq 0
      then
        echo "------------------------------------------------- OK"
      else
        echo "ERROR ------------------------------ ERROR"
        echo ${FILE_NAME} --- ${MODEL_FILE}     --- Seem to be different
      fi
  else
      echo 'ERROR ------------------------------ ERROR'
      echo "Expected ${FILE_NAME} not found."
  fi
}



compare_directories(){
  TARGET_DIRECTORY_NAME=$1
  REFERENCE_DIRECTORY_NAME=$2

  # Checks whether both directories have identical content
  TARGET_DIRECTORY_NAME_LENGTH=${#TARGET_DIRECTORY_NAME}
  targetContent=$(
    find ${TARGET_DIRECTORY_NAME} -type f |
    cut -c$((${TARGET_DIRECTORY_NAME_LENGTH}+2))-
    )

  REFERENCE_DIRECTORY_NAME_LENGTH=${#REFERENCE_DIRECTORY_NAME}
  referenceContent=$(
    find ${REFERENCE_DIRECTORY_NAME} -type f |
    cut -c$((${REFERENCE_DIRECTORY_NAME_LENGTH}+2))-
    )

  STATUS='OK'
  for file in $(\
    echo "${targetContent} ${referenceContent}" \
    | tr ' ' '\n' \
    | sort -u
    )
  do
    ZDIFF_OUTPUT=$(\
      zdiff ${TARGET_DIRECTORY_NAME}/${file} \
      ${REFERENCE_DIRECTORY_NAME}/${file})
    if test $? -ne 0
    then
      STATUS='NOK'
      echo -e '\t'${TARGET_DIRECTORY_NAME}/${file}
      echo -e '\t'"${ZDIFF_OUTPUT}"
    #else
      #echo -e '\t'${TARGET_DIRECTORY_NAME}/${file}
      #echo -e '\t'"OK"
    fi
  done

  if test $STATUS = 'OK'
  then
    echo "------------------------------------------------- OK"
  else
    echo "====================================================== FAIL"
  fi
}



# Creates and cleans test directory structure
if true; then
  if [ ! -d "test" ]; then

    mkdir test
    mkdir test/scripts
    mkdir test/inputs
    mkdir test/tmp
    mkdir test/outputs

  else

    if [ ! -d "test/scripts" ]; then
    mkdir test/scripts
    fi

    if [ ! -d "test/inputs" ]; then
    mkdir test/inputs
    fi

    if [ ! -d "test/tmp" ]; then
    mkdir test/tmp
    else
    rm -fR test/tmp/*
    fi

    if [ ! -d "test/outputs" ]; then
    mkdir test/outputs
    else
    rm -fR test/outputs/*
    fi

  fi
else
  echo "WARNING -- TESTING MODE"
fi

run_tests
