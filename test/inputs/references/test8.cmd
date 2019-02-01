#!/bin/bash
#SBATCH --job-name=UPF_tasks_cpus
#SBATCH --output=./test/outputs/UPF_tasks_cpus_%j.out
#SBATCH --error=./test/outputs/UPF_tasks_cpus_%j.err
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=3

ls -ald *
