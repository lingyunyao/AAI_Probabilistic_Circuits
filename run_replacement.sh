#!/bin/bash

#SBATCH --time=5-00:00:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=1G
#SBATCH --output=myjob_output.log
#SBATCH --array=1-40
echo "SLURM script starting..."
echo "Cluster: " $SLURM_CLUSTER_NAME
echo "Job Name: " $SLURM_JOB_NAME
echo "Job ID: " $SLURM_JOBID
echo "On Node: " $SLURMD_NODENAME
echo "Array Task ID: " $SLURM_ARRAY_TASK_ID

# Array definitions
#'nltcs' 'jester' 'dna' 
datasets=('nltcs' 'jester' 'dna' 'book')
percentages=( 0.2 0.4 0.6 0.8 1.0)
#percentages=(0.0)
selection_methods=( 'random')
det_methods=('nondet' 'det')

# Calculate total number of combinations
total_combinations=$(( ${#datasets[@]} * ${#percentages[@]} * ${#selection_methods[@]} * ${#det_methods[@]} ))

# Check if the task ID is within bounds
if [ "$SLURM_ARRAY_TASK_ID" -le "$total_combinations" ]; then
    # Calculate parameter indices
    index=$SLURM_ARRAY_TASK_ID
    method_index=$(( (index-1) % ${#det_methods[@]} ))
    index=$(( (index-1) / ${#det_methods[@]} ))
    s_index=$(( index % ${#selection_methods[@]} ))
    index=$(( index / ${#selection_methods[@]} ))
    p_index=$(( index % ${#percentages[@]} ))
    dataset_index=$(( index / ${#percentages[@]} ))

    # Extract the parameters
    dataset=${datasets[$dataset_index]}
    p=${percentages[$p_index]}
    s=${selection_methods[$s_index]}
    method=${det_methods[$method_index]}

    # Log
    echo "Dataset: $dataset"
    echo "P: $p"
    echo "S: $s"
    echo "Method: $method"

    # Run the Python script
    srun python3.6 replacement.py $dataset $p $s $method
else
    echo "Array Task ID out of range."
fi

echo "SLURM script completed."