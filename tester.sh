#!/bin/bash

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
		mkdir test/scrips
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

#*************************************************************************************************

python test/scripts/tester_launch.py
