#!/bin/bash
#SBATCH --job-name=upfBasic
#SBATCH --output=./test/outputs/upfBasic_%j.out
#SBATCH --error=./test/outputs/upfBasic_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

ls -al
