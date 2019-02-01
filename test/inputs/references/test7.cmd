#!/bin/bash
#SBATCH --job-name=timeModulesUPF
#SBATCH --output=./test/outputs/timeModulesUPF_%j.out
#SBATCH --error=./test/outputs/timeModulesUPF_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=05:00:00
module load GZIP
module load SRA

gzip -d bigfile.fastq
