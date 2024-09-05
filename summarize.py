import os
import pandas as pd
import csv

accuracy_dir = "accuracy/greedy_change_proneness"
summary_dir = "results/greedy_change_proneness/summary"

for budget in os.listdir(accuracy_dir):
    
    budget_dir = os.path.join(accuracy_dir, budget)
    
    accuracy_mean = []
    fdr_mean = []
    accuracy_total = []
    fdr_total = []
    accuracy_min = []
    fdr_min = []
    accuracy_max = []
    fdr_max = []

    output_file = f"{summary_dir}/{budget}.csv"
    # crate a file named upon project if it doesn't exist
    if not os.path.exists(output_file):
        file = open(output_file, 'w')
        writer = csv.writer(file)
        writer.writerow(["Project", "Accuracy_Min", "FDR_Min", "Accuracy_Max", "FDR_Max", "Accuracy_Mean", "FDR_Mean", "Accuracy_Total", "FDR_Total"])
        file.close()

    for project in os.listdir(budget_dir):
        project_name = project.split('.')[0]
        project_results = pd.read_csv(f"{budget_dir}/{project}")
        
        min_accuracy = project_results[project_results['Strategy'] == 'Min']['Accuracy'].mean()
        min_fdr = project_results[project_results['Strategy'] == 'Min']['FDR'].mean()
        max_accuracy = project_results[project_results['Strategy'] == 'Max']['Accuracy'].mean()
        max_fdr = project_results[project_results['Strategy'] == 'Max']['FDR'].mean()
        mean_accuracy = project_results[project_results['Strategy'] == 'Mean']['Accuracy'].mean()
        mean_fdr = project_results[project_results['Strategy'] == 'Mean']['FDR'].mean()
        total_accuracy = project_results[project_results['Strategy'] == 'Total']['Accuracy'].mean()
        total_fdr = project_results[project_results['Strategy'] == 'Total']['FDR'].mean()

        accuracy_max.append(max_accuracy)
        fdr_max.append(max_fdr)
        accuracy_min.append(min_accuracy)
        fdr_min.append(min_fdr)
        accuracy_mean.append(mean_accuracy)
        fdr_mean.append(mean_fdr)
        accuracy_total.append(total_accuracy)
        fdr_total.append(total_fdr)

        with open(output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([project_name, min_accuracy, min_fdr, max_accuracy, max_fdr, mean_accuracy, mean_fdr, total_accuracy, total_fdr])
            f.close()

    strategies = {
        "Min Accuracy": accuracy_min,
        "Min FDR": fdr_min,
        "Max Accuracy": accuracy_max,
        "Max FDR": fdr_max,
        "Mean Accuracy": accuracy_mean,
        "Mean FDR": fdr_mean,
        "Total Accuracy": accuracy_total,
        "Total FDR": fdr_total
    }
    
    max_mean_accuracy = 0
    max_mean_accuracy_strategy = ""
    max_mean_fdr = 0
    max_mean_fdr_strategy = ""
    # calculate the mean of the accuracy and fdr for each strategy and show the stats, 25 percentile, median, 75 percentile, mean and standard deviation
    print(f"\nStatistics for budget: {budget}")
    for strategy, values in strategies.items():
        values = pd.Series(values)
        
        percentile_25 = values.quantile(0.25)
        median = values.median()
        percentile_75 = values.quantile(0.75)
        mean = values.mean()
        std_dev = values.std()
        
        if "Accuracy" in strategy:
            if mean > max_mean_accuracy:
                max_mean_accuracy = mean
                max_mean_accuracy_strategy = strategy
        else:
            if mean > max_mean_fdr:
                max_mean_fdr = mean
                max_mean_fdr_strategy = strategy

        # print(f"{strategy}:")
        # print(f"  25th Percentile: {percentile_25}")
        # print(f"  Median: {median}")
        # print(f"  75th Percentile: {percentile_75}")
        # print(f"  Mean: {mean}")
        # print(f"  Standard Deviation: {std_dev}")
        # print("---------------------------------------------------")

    print(f"Strategy with the highest mean accuracy: {max_mean_accuracy_strategy} with mean accuracy: {max_mean_accuracy}")
    print(f"Strategy with the highest mean FDR: {max_mean_fdr_strategy} with mean FDR: {max_mean_fdr}")
