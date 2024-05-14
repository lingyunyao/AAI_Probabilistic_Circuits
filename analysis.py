import os
import json
import csv
import numpy as np
from collections import defaultdict
# Compute the normalized energy according to the energy model
def compute_x_values(percentages):
    part1 = 0.0328 * ((52 + 1)**2) * np.log(52 + 1) + 0.5469 * 11
    part2 = 0.0520160465095606 * (52 + 11)
    return [p * part1 + (1 - p) * part2 for p in percentages]


# for file saving
def save_to_csv(data, filename="output.csv", headers=["X-Value", "Y-Value", "Trace Name"]):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(headers)
        # Write data rows
        for row in data:
            writer.writerow(row)


#Process replacement results
# 1. Define the parameters
datasets = ['nltcs', 'jester', 'dna', 'book']
percentages = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
selection_methods = ['small', 'random']
det_methods = ['det', 'nondet']


# 2. Data structure to hold results
results = {}

# 3. Read the files
for dataset in datasets:
    for p in percentages:
        for s in selection_methods:
            for method in det_methods:
                filename = f'./results/results_replacement_{dataset}_{p}_{s}_{method}.txt'
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        data = json.load(f)
                        key = f"{dataset}_{p}_{s}_{method}"
                        if key in data:
                            results[key] = data[key]

# Calculate the normalized energy using actual_percentage
energy_actualpercentages = {}

for dataset in datasets:
    for s in selection_methods:
        for method in det_methods:
            key_format = f"{dataset}_{{}}_{s}_{method}"
            energy_actualpercentages[key_format] = [
                (1-results.get(key_format.format(p), {}).get('actual_percentage', p)) * 
                (0.0328 * ((52 + 1)**2) * np.log(52 + 1) + 0.5469 * 11) + 
                (results.get(key_format.format(p), {}).get('actual_percentage', p)) * 
                0.0520160465095606 * (52 + 11)
                for p in percentages
            ]

# Compute the energy value of without replacement
x_for_one = (1 ) * (0.0328 * ((52 + 1)**2) * np.log(52 + 1) + 0.5469 * 11) + (0) * 0.0520160465095606 * (52 + 11)
for key, x_values in energy_actualpercentages.items():
    normalized_values = np.array(x_values) / x_for_one
    energy_actualpercentages[key] = normalized_values.tolist()

# Store data for CSV
csv_data = []

for idx, dataset in enumerate(datasets):
    for combo in [(s, method) for s in selection_methods for method in det_methods]:
        s, method = combo
        key_format = f"{dataset}_{{}}_{s}_{method}"
        y_values = [results.get(key_format.format(p), {}).get('numerical_loss_before', None) for p in percentages]
        trace_name = f"{s}-{method}"
        for x, y in zip(energy_actualpercentages[key_format], y_values):
            if y is not None:  # Ensure we have a valid y-value        
                csv_data.append([x, y, trace_name])

# Define custom headers and filename
headers = ["energy", "error", "replacement_method"]
filename = "replacement.csv"

# Save data to CSV
save_to_csv(csv_data, filename=filename, headers=headers)

















# Process MAP/MAR result

# parameters
datasets = ['nltcs', 'jester', 'dna', 'book']
e_values = [8,9,10,11]
m_values = [2,3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
data_types = ['app','float']
evaluation_metrics = [ 'MAR','MAP']

# hold results
results = {dataset: {} for dataset in datasets}

# Read the files
for dataset in datasets:
    for e in e_values:
        for m in m_values:
            for data_type in data_types:
                for metric in evaluation_metrics:
                    filename = f'./results/results_accuracy_{dataset}_{e}_{m}_{data_type}_{metric}.txt'
                    if os.path.exists(filename):
                        with open(filename, 'r') as f:
                            data = json.load(f)
                            key = f"{dataset}_{e}_{m}_{data_type}_{metric}"
                            if key in data:
                                results[dataset][(e, m, data_type, metric)] = {
                                    'numerical_loss_after': data[key]['numerical_loss_after'],
                                    'string_accuracy': data[key]['string_accuracy']
                                }


csv_data = []  # List to collect data for CSV

for idx_dataset, dataset in enumerate(datasets):
    for idx_metric, metric in enumerate(evaluation_metrics):
        for idx_e, e in enumerate(e_values):
            
            # Calculate x-values
            raw_x_values_float = [0.0328 * ((m + 1)**2) * np.log(m + 1) + 0.5469 * e for m in m_values]
            raw_x_values_app = [0.0520160465095606 * (m + e) for m in m_values]
            x_values_float = np.array(raw_x_values_float) / x_for_one
            x_values_app = np.array(raw_x_values_app) / x_for_one            
            for data_type, x_values in [('float', x_values_float), ('app', x_values_app)]:
                if metric == "MAP":
                    y_values = [results[dataset].get((e, m, data_type, metric), {}).get('string_accuracy', None) for m in m_values]
                else:  # MAR
                    y_values = [results[dataset].get((e, m, data_type, metric), {}).get('numerical_loss_after', None) for m in m_values]
                for m, x, y in zip(m_values, x_values, y_values):
                    if y is not None:
                        csv_data.append([dataset, e, m, data_type, metric, x, y])  # Collect data for CSV


# Saving the collected data to CSV
csv_filename = "MAP_MAR_data.csv"
headers = ["Dataset", "E value", "M value", "Data Type", "Metric", "energy", "accuracy/error"]
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # Write the header
    for row in csv_data:
        writer.writerow(row)  # Write the actual rows 





# Assume csv_data is already filled with the data
data_grouped = defaultdict(list)
# Group data by (Dataset, E value, Metric, Data Type)
for row in csv_data:
    key = (row[0], row[1], row[3], row[4])  # (Dataset, E value, Data Type, Metric)
    data_grouped[key].append((row[5], row[6]))  # Append (energy, accuracy/error)

output_strings = []
for (dataset, e_val, data_type, metric), values in data_grouped.items():
    header = f"% Dataset: {dataset}\n% E value: {e_val}\n% Metric: {metric}\n% Data type: {data_type}\n\n"
    body = "        {\n            \\\\\n" + "\n".join([f"            {x:.5f}  {y:.5f}  \\\\" for x, y in values]) + "\n        }\n        ;"
    output_strings.append(header + body)

# Write to a file
with open('formatted_data_plot.txt', 'w') as file:
    file.write("\n".join(output_strings))



# Assume csv_data is already filled with the data
data_grouped = defaultdict(list)
# Group data by (Dataset, E value, Metric, Data Type)
for row in csv_data:
    key = (row[0], row[1], row[3], row[4])  # (Dataset, E value, Data Type, Metric)
    m_value = float(row[2])  # Convert M value to float for formatting
    data_grouped[key].append((m_value, row[6]))  # Append (M value, accuracy/error)

output_strings = []
for (dataset, e_val, data_type, metric), values in data_grouped.items():
    header = f"% Dataset: {dataset}\n% E value: {e_val}\n% Metric: {metric}\n% Data type: {data_type}\n\n"
    body = "        {\n            \\\\\n" + "\n".join([f"            {m:.1f}  {y:.5f}  \\\\" for m, y in values]) + "\n        }\n        ;"
    output_strings.append(header + body)
# Write to a file
with open('formatted_data_with_m_values.txt', 'w') as file:
    file.write("\n".join(output_strings))





