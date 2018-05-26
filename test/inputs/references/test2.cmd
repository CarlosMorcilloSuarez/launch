#!/bin/bash
# @ job_name = unzip003
# @ initialdir = .
# @ output = unzip003_%j.out
# @ error = unzip003_%j.err
# @ total_tasks = 1
# @ cpus_per_task = 1
# @ wall_clock_limit = 05:00:00

module load GZIP
module load SRA

gzip -d bigfile.fastq
