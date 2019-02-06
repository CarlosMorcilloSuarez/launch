#!/bin/bash
#SBATCH --job-name=UPF_memory
#SBATCH --output=./test/outputs/UPF_memory_%j.out
#SBATCH --error=./test/outputs/UPF_memory_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000

ls -al
