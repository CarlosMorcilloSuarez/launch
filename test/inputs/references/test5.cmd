#!/bin/bash
# @ job_name = simplifiedSpaces
# @ initialdir = .
# @ output = ./test/outputs/simplifiedSpaces_%j.out
# @ error = ./test/outputs/simplifiedSpaces_%j.err
# @ total_tasks = 1
# @ cpus_per_task = 1
# @ wall_clock_limit = 1:00:00


 
 ls -alh *.txt
 mv veryLongFile.txt veryVeryLongFile.txt 
