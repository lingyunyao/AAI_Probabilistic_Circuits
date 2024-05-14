#!/bin/bash

#SBATCH --time=2:00:00
##SBATCH --nodes=4
#SBATCH --mem-per-cpu=1G
#SBATCH --output=myjob_output_1.log
#SBATCH --array=1-4

echo "SLURM script starting..."
echo "Cluster: " $SLURM_CLUSTER_NAME
echo "Job Name: " $SLURM_JOB_NAME
echo "Job ID: " $SLURM_JOBID
echo "On Node: " $SLURMD_NODENAME
echo "Array Task ID: " $SLURM_ARRAY_TASK_ID


# Array definitions
datasets=('nltcs' 'jester' 'dna' 'book')


# Select dataset based on the SLURM_ARRAY_TASK_ID
dataset=${datasets[$SLURM_ARRAY_TASK_ID - 1]}

# Now run your Python script with the selected dataset
python3.6 sampling.py $dataset

echo "SLURM script completed."


