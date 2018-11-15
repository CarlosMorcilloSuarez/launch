#!/bin/bash
# @ job_name = low_priority_queue
# @ initialdir = .
# @ output = ./test/outputs/low_priority_queue_%j.out
# @ error = ./test/outputs/low_priority_queue_%j.err
# @ total_tasks = 1
# @ cpus_per_task = 1
# @ wall_clock_limit = 35:00:00
# @ class = lowprio


ls -ald *
