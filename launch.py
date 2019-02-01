#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
launch.py

    Wrapper to submit jobs to the CNAG and UPF clusters.
    First it creates a Command File according to the especifications received
        from command line arguments.
    Then submits that command file to the cluster to be executed.
'''

__author__ = "Carlos Morcillo-Suarez"
__license__ = "GPL"
__version__ = "1.5"
__email__ = "carlos.morcillo.upf.edu@gmail.com"

import sys
import os

import subprocess
import getopt
import unittest
import re

import launchConfig

def usage():
    print """
    launch

        Is a wrapper to submit jobs to the CNAG and UPF clusters.
        First it creates a Command File according to the especifications received
            from command line arguments.
        Then submits that command file to the cluster to be executed.
        
        The cluster (CNAG or UPF) where launch is running must be specified 
            in the launchconfig.py file.

        Use
            launch [options] -c command_to_execute

        Options
            -h, --help
                Shows this help message

            -c, --command
                The command that will be included in the file to be
                executed in the cluster

            -n, --name
                Name that will be used to create the command file
                and job name.
                Default = "job"

            -l, --limit
                wall-clock-limit. Maximum amount of time that the
                job will be allowd to run on the cluster.
                --limit hh:mm:ss
                Default = 01:00:00 (CNAG)
                          No limit (UPF)

            -t, --tasks
                total_tasks*cpus_per_task

                example:
                --tasks 1*2
                    total_tasks = 1
                    cpus_per_task = 2

                Default = 1*1

            -m, --modules
                modules to be added in the execution of the job.
                --modules "MODUL1 MODUL2"

            -f, --file-only
                only creates the file and does not execute it after creation

            -o, --output-directory
                directory where the command, output and stderr files are
                created.
                Default = '.'

            -v, --version
                Displays version

            -d, --dependent-on
                -d <job_id>:<job_id> ...
                mnsubmit will be called as:
                    mnsubmit -dep afterok:<job_id>:<job_id>...

                The job will not begin execution until all the specified
                job_IDs have successfuly ended



        Examples
            (CNAG cluster)
            launch --name dog1qc -c "fastqc -i ./dog1.fastq -o ./dog1"
                generates a file "doglqc.cmd" with content:

                    #!/bin/bash
                    # @ job_name = dog1qc
                    # @ initialdir = .
                    # @ output = dog1qc_%j.out
                    # @ error = dog1qc_%j.err
                    # @ total_tasks = 1
                    # @ cpus_per_task = 1
                    # @ wall_clock_limit = 01:00:00

                    fastqc -i ./dog1.fastq -o ./dog1

            launch --name unzip003 --limit 05:00:00 --modules "GZIP SRA" -c "gzip -d bigfile.fastq"
                generates a file "unzip003.cmd" with content:

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


            (UPF cluster)
            ./launch --file-only --name UPF_tasks_cpus --tasks 2*3 --output-directory ./test/outputs -c "ls -ald *"
                generates a file "UPF_tasks_cpus.cmd" with content
                
                    #!/bin/bash
                    #SBATCH --job-name=UPF_tasks_cpus
                    #SBATCH --output=./test/outputs/UPF_tasks_cpus_%j.out
                    #SBATCH --error=./test/outputs/UPF_tasks_cpus_%j.err
                    #SBATCH --ntasks=2
                    #SBATCH --cpus-per-task=3

                    ls -ald *
        """
        
        
class JobDefinition():    
    def __init__(self):
        self.clusterName = launchConfig.clusterName
        self.name = 'job'
        self.previousJobs = ''
        self.commandToExecute = ''
        if launchConfig.clusterName=="CNAG":
            self.limit = "01:00:00"
        elif launchConfig.clusterName=="UPF":
            self.limit = None
        self.total_tasks = '1'
        self.cpus_per_task = '1'
        self.modules = []
        self.executeFile = True
        self.outputDirectory = '.'


def processArguments(jobDefinition,argv):
    try:
        opts, args = getopt.getopt(
                        argv,
                        "hn:l:t:m:c:fo:vd:",
                        ["help", "name=", "limit=",
                        "tasks=","modules=","command=",
                        "file-only","output-directory=",
                        "version","dependent-on="]
        )
    except getopt.GetoptError as e:
        print e
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-v", "--version"):
            print('launch Version: '+__version__)
            sys.exit()
        elif opt in ("-n", "--name"):
            jobDefinition.name = arg
        elif opt in ("-l", "--limit"):
            jobDefinition.limit = arg
        elif opt in ("-t", "--tasks"):
            jobDefinition.total_tasks , jobDefinition.cpus_per_task = arg.split('*')
        elif opt in ("-m", "--modules"):
            jobDefinition.modules = arg.split()
        elif opt in ("-c", "--command"):
            jobDefinition.commandToExecute = arg
        elif opt in ("-f", "--file-only"):
            jobDefinition.executeFile = False
        elif opt in ("-o", "--output-directory"):
            jobDefinition.outputDirectory = arg
        elif opt in ("-d", "--dependent-on"):
            jobDefinition.previousJobs = arg

def writeCommandFile(jobDefinition, clusterName):
    commandFileName = os.path.join(jobDefinition.outputDirectory,jobDefinition.name+".cmd")
    jobName = jobDefinition.name

    # Simplifies blank spaces in commandToExecute
    jobDefinition.commandToExecute = re.sub(' +',' ',jobDefinition.commandToExecute)

    try:
        with open(commandFileName,"w") as commandFile:
            commandFile.write("#!/bin/bash\n")

            if clusterName=="CNAG":
                # Cluster parameters
                commandFile.write("# @ job_name = "+jobName+"\n")
                commandFile.write("# @ initialdir = .\n")
                commandFile.write("# @ output = "+jobDefinition.outputDirectory+"/"+jobName+"_%j.out\n")
                commandFile.write("# @ error = "+jobDefinition.outputDirectory+"/"+jobName+"_%j.err\n")
                commandFile.write("# @ total_tasks = "+jobDefinition.total_tasks+"\n")
                commandFile.write("# @ cpus_per_task = "+jobDefinition.cpus_per_task+"\n")
                commandFile.write("# @ wall_clock_limit = "+jobDefinition.limit+"\n")
                # Assigns the job to low priority queue if execution time
                # Is greater than 24 hours.
                if 24 <= int(jobDefinition.limit.split(':')[0]):
                     commandFile.write("# @ class = lowprio\n")
                commandFile.write("\n")

            if clusterName=="UPF":
                # Cluster parameters
                commandFile.write("#SBATCH --job-name="+jobName+"\n")
                commandFile.write("#SBATCH --output="+jobDefinition.outputDirectory+"/"+jobName+"_%j.out\n")
                commandFile.write("#SBATCH --error="+jobDefinition.outputDirectory+"/"+jobName+"_%j.err\n")
                commandFile.write("#SBATCH --ntasks="+jobDefinition.total_tasks+"\n")
                commandFile.write("#SBATCH --cpus-per-task="+jobDefinition.cpus_per_task+"\n")
                if jobDefinition.limit:
                    commandFile.write("#SBATCH --time="+jobDefinition.limit+"\n")



            # Modules
            for module in jobDefinition.modules:
                commandFile.write("module load "+module+"\n")

            # Command
            commandFile.write("\n")
            commandFile.write(jobDefinition.commandToExecute+"\n")
                        
    except Exception as e:
        print e
    
    return commandFileName
    
    
if __name__ == "__main__":

    jobDefinition = JobDefinition()

    # Process command line
    processArguments(jobDefinition,sys.argv[1:])

    # Ends execution if commands were not especified.
    if jobDefinition.commandToExecute == "":
        print "No Commands to execute (--command) were especified"
        print
        usage()
        sys.exit(2)

    # Creates Command File
    commandFileName = writeCommandFile(jobDefinition,launchConfig.clusterName)

    # Executes Command File
    if jobDefinition.executeFile:
        
        if launchConfig.clusterName=="CNAG":
            if jobDefinition.previousJobs == '':
                command = "mnsubmit "+commandFileName
                result = subprocess.check_output(command, shell=True)            
            else:
                command = "mnsubmit -dep afterok:"+jobDefinition.previousJobs+' '+commandFileName
                result = subprocess.check_output(command, shell=True)
            print result.split()[3]+" "+result
            
        if launchConfig.clusterName=="UPF":
           if jobDefinition.previousJobs == '':
               command = "sbatch "+commandFileName
               result = subprocess.check_output(command, shell=True) 
           else:
               command = "sbatch --dependency afterok:"+jobDefinition.previousJobs+' '+commandFileName
               result = subprocess.check_output(command, shell=True) 
           print result.split()[3]+" "+result
        
