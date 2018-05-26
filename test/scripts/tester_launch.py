#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import shlex, subprocess


class TestData():
    def __init__(self):
        self.title=''
        self.type = ''
        self.output = ''
        self.reference = ''
        self.command = ''

def runTest(testData):
    outputFile = testData.output
    referenceFile = testData.reference

    # Eliminates outputFile if it exists
    if os.path.isfile(outputFile):
        os.remove(outputFile)

    print '--------------------------------------------'
    print testData.title

    # Executes command
    subprocess.call(shlex.split(testData.command))

    # Compares obtained file with reference
    status = subprocess.call(['diff', outputFile, referenceFile])
    if status == 0:
        print 'OK'
    else:
        print
        print '----------------- FAIL'
    print


# Test ################################################
test = TestData()

# -- Test definition
test.title='Basic test'
test.type = 'F'

test.output = './test/outputs/zdog1qc.cmd'
test.reference = './test/inputs/references/test1.cmd'

test.command = './launch \
                    --file-only \
                    --name zdog1qc \
                    --output-directory ./test/outputs \
                    -c "fastqc -i ./dog1.fastq -o ./dog1" \
                 '

# -- Execute Test
runTest(test)


# Test ################################################
test = TestData()

# -- Test definition
test.title='Time Limit and modules test'
test.type = 'F'

test.output = './test/outputs/unzip003.cmd'
test.reference = './test/inputs/references/test2.cmd'

test.command = './launch \
                    --file-only \
                    --name unzip003 \
                    --limit 05:00:00 \
                    --modules "GZIP SRA" \
                    --output-directory ./test/outputs \
                    -c "gzip -d bigfile.fastq" \
                '

# -- Execute Test
runTest(test)

# Test ################################################
test = TestData()

# -- Test definition
test.title='tasks and cpus per task'
test.type = 'F'

test.output = './test/outputs/tasks_and_cpus.cmd'
test.reference = './test/inputs/references/test3.cmd'

test.command = './launch \
                    --file-only \
                    --name tasks_and_cpus \
                    --tasks 2*3 \
                    --output-directory ./test/outputs \
                    -c "ls -ald *" \
                '

# -- Execute Test
runTest(test)

# Test ################################################
test = TestData()

# -- Test definition
test.title='Low priority queue for long jobs'
test.type = 'F'

test.output = './test/outputs/low_priority_queue.cmd'
test.reference = './test/inputs/references/test4.cmd'

test.command = './launch \
                    --file-only \
                    --name low_priority_queue \
                    --limit 35:00:00 \
                    --output-directory ./test/outputs \
                    -c "ls -ald *" \
                '

# -- Execute Test
runTest(test)
