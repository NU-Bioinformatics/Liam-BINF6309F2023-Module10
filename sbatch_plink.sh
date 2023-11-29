#!/bin/bash
#SBATCH --partition=short               # choose from debug, express, or short
#SBATCH --job-name=plink tutorial
#SBATCH --time=04:00:00                 # the code pieces should run in far less than 4 hours
#SBATCH -N 1                            # nodes requested
#SBATCH -n 1                            # task per node requested
#SBATCH --output="plink_tutorial.output"   # where to direct standard output; will be batch-jobname-jobID.output

bash getExamples.sh

bash plinkHapmap1.sh

echo "analysis complete"

