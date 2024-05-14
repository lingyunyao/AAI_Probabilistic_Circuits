#!/bin/bash

#SBATCH --time=1-01:00:00
##SBATCH --nodes=1
#SBATCH --mem-per-cpu=1G
#SBATCH --output=myjob_output_1.log
#SBATCH --array=1-320

echo "SLURM script starting..."
echo "Cluster: " $SLURM_CLUSTER_NAME
echo "Job Name: " $SLURM_JOB_NAME
echo "Job ID: " $SLURM_JOBID
echo "On Node: " $SLURMD_NODENAME
echo "Array Task ID: " $SLURM_ARRAY_TASK_ID

 
# Array definitions
datasets=('nltcs' 'jester' 'dna' 'book')
e_values=( 8 9 10 11)
m_values=(2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21)
data_types=( 'app' )
evaluation_metrics=('MAR' )

# Calculate total number of combinations
total_combinations=$(( ${#datasets[@]} * ${#e_values[@]} * ${#m_values[@]} * ${#data_types[@]} * ${#evaluation_metrics[@]} ))

# Check if the task ID is within bounds
if [ "$SLURM_ARRAY_TASK_ID" -le "$total_combinations" ]; then
    # Calculate parameter indices
    index=$SLURM_ARRAY_TASK_ID
    metric_index=$(( (index-1) % ${#evaluation_metrics[@]} ))
    index=$(( (index-1) / ${#evaluation_metrics[@]} ))
    data_type_index=$(( index % ${#data_types[@]} ))
    index=$(( index / ${#data_types[@]} ))
    m_index=$(( index % ${#m_values[@]} ))
    index=$(( index / ${#m_values[@]} ))
    e_index=$(( index % ${#e_values[@]} ))
    dataset_index=$(( index / ${#e_values[@]} ))

    # Extract the parameters
    dataset=${datasets[$dataset_index]}
    e=${e_values[$e_index]}
    m=${m_values[$m_index]}
    data_type=${data_types[$data_type_index]}
    metric=${evaluation_metrics[$metric_index]}

    # Log
    echo "Dataset: $dataset"
    echo "E: $e"
    echo "M: $m"
    echo "Data type: $data_type"
    echo "Metric: $metric"

    # Run the Python script
    srun python3.6 AAI_experiments_SPN.py $dataset $e $m $data_type $metric 
else
    echo "Array Task ID out of range."
fi

echo "SLURM script completed."






# Run the Python script
srun python3.6 AAI_experiments_SPN.py $dataset $e $m $data_type $metric 
echo "SLURM script completed."
