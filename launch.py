#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
launch.py

    Wrapper to submit jobs to the CNAG cluster.
    First it creates a Command File according to the especifications received
        from command line arguments.
    Then submits that command file to the cluster to be executed.
'''

__author__ = "Carlos Morcillo-Suarez"
__copyright__ = "Copyright 2018, Carlos Morcillo-Suarez"
__license__ = "GPL"
__version__ = "1.2"
__email__ = "carlos.morcillo.upf.edu@gmail.com"

import sys
import os

import getopt
import unittest
import re


def usage():
    print """
    launch

        Creates a command file with the approapriate format to be
        launched as a job in CNAG cluster and submits the file as a
        job using
            $ mnsubmit command.

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
                Default = 01:00:00

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
                directory where the *.cmd file is created
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

        """


def processArguments(argv):
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
            global name
            name = arg
        elif opt in ("-l", "--limit"):
            global limit
            limit = arg
        elif opt in ("-t", "--tasks"):
            global total_tasks
            global cpus_per_task
            total_tasks , cpus_per_task = arg.split('*')
        elif opt in ("-m", "--modules"):
            global modules
            modules = arg.split()
        elif opt in ("-c", "--command"):
            global commandToExecute
            commandToExecute = arg
        elif opt in ("-f", "--file-only"):
            global executeFile
            executeFile = False
        elif opt in ("-o", "--output-directory"):
            global outputDirectory
            outputDirectory = arg
        elif opt in ("-d", "--dependent-on"):
            global previousJobs
            previousJobs = arg


if __name__ == "__main__":

    name = 'job'
    previousJobs = ''
    commandToExecute = ''
    limit = "01:00:00"
    total_tasks = '1'
    cpus_per_task = '1'
    modules = []
    executeFile = True
    outputDirectory = '.'

    # Process command line
    processArguments(sys.argv[1:])

    # Ends execution if commands were not especified.
    if commandToExecute == "":
        print "No Commands to execute (--command) were especified"
        print
        usage()
        sys.exit(2)

    # Creates Command File
    commandFileName = os.path.join(outputDirectory,name+".cmd")
    jobName = name

    # Simplifies blank spaces in commandToExecute
    commandToExecute = re.sub(' +',' ',commandToExecute)

    try:
        with open(commandFileName,"w") as commandFile:
            commandFile.write("#!/bin/bash\n")

            # Cluster parameters
            commandFile.write("# @ job_name = "+jobName+"\n")
            commandFile.write("# @ initialdir = .\n")
            commandFile.write("# @ output = "+jobName+"_%j.out\n")
            commandFile.write("# @ error = "+jobName+"_%j.err\n")
            commandFile.write("# @ total_tasks = "+total_tasks+"\n")
            commandFile.write("# @ cpus_per_task = "+cpus_per_task+"\n")
            commandFile.write("# @ wall_clock_limit = "+limit+"\n")
            # Assigns the job to low priority queue if execution time
            # Is greater than 24 hours.
            if 24 <= int(limit.split(':')[0]):
                 commandFile.write("# @ class = lowprio\n")
            commandFile.write("\n")

            # Modules
            for module in modules:
                commandFile.write("module load "+module+"\n")

            # Command
            commandFile.write("\n")
            commandFile.write(commandToExecute+"\n")
    except Exception as e:
        print e


    # Executes Command File
    if executeFile:
        if previousJobs == '':
            os.system("mnsubmit "+commandFileName)
        else:
            os.system("mnsubmit -dep afterok:"+previousJobs+' '+commandFileName)
