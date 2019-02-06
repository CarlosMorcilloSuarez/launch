#!/bin/bash
# @ job_name = CNAG_memory
# @ initialdir = .
# @ output = ./test/outputs/CNAG_memory_%j.out
# @ error = ./test/outputs/CNAG_memory_%j.err
# @ total_tasks = 1
# @ cpus_per_task = 1
# @ wall_clock_limit = 01:00:00
# @ memory = 10000


fastqc -i ./dog1.fastq -o ./dog1
