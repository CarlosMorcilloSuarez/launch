#!/bin/bash
# @ job_name = zdog1qc
# @ initialdir = .
# @ output = zdog1qc_%j.out
# @ error = zdog1qc_%j.err
# @ total_tasks = 1
# @ cpus_per_task = 1
# @ wall_clock_limit = 01:00:00


fastqc -i ./dog1.fastq -o ./dog1
