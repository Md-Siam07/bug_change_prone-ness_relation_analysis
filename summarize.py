import os
import pandas as pd
import csv

accuracy_dir = "accuracy/greedy_stable_with_previous_buggy"
summary_dir = f"{accuracy_dir}/summary"

if not os.path.exists(summary_dir):
    os.makedirs(summary_dir)

for budget in [25,50,75]:
    
    budget_dir = os.path.join(accuracy_dir, str(budget))
    if not os.path.isdir(budget_dir):
        os.makedirs(budget_dir)

    accuracy_mean = []
    fdr_mean = []
    accuracy_total = []
    fdr_total = []
    accuracy_min = []
    fdr_min = []
    accuracy_max = []
    fdr_max = []
    accuracy_mean_lines = []
    fdr_mean_lines = []
    accuracy_total_lines = []
    fdr_total_lines = []
    accuracy_min_lines = []
    fdr_min_lines = []
    accuracy_max_lines = []
    fdr_max_lines = []


    output_file = f"{summary_dir}/{budget}.csv"
    # crate a file named upon project if it doesn't exist
    if not os.path.exists(output_file):
        file = open(output_file, 'w')
        writer = csv.writer(file)
        writer.writerow(["Project", "Accuracy_Min", "FDR_Min", "Accuracy_Max", "FDR_Max", "Accuracy_Mean", "FDR_Mean", "Accuracy_Total", "FDR_Total", "Accuracy_Min_Lines", "FDR_Min_Lines", "Accuracy_Max_Lines", "FDR_Max_Lines", "Accuracy_Mean_Lines", "FDR_Mean_Lines", "Accuracy_Total_Lines", "FDR_Total_Lines"])
        file.close()

    for project in os.listdir(budget_dir):
        project_name = project.split('.')[0]
        project_results = pd.read_csv(f"{budget_dir}/{project}")
        # print(f"{budget_dir}/{project}")
        min_accuracy = project_results[project_results['Strategy'] == 'Min']['Accuracy'].mean()
        min_fdr = project_results[project_results['Strategy'] == 'Min']['FDR'].mean()
        max_accuracy = project_results[project_results['Strategy'] == 'Max']['Accuracy'].mean()
        max_fdr = project_results[project_results['Strategy'] == 'Max']['FDR'].mean()
        mean_accuracy = project_results[project_results['Strategy'] == 'Mean']['Accuracy'].mean()
        mean_fdr = project_results[project_results['Strategy'] == 'Mean']['FDR'].mean()
        total_accuracy = project_results[project_results['Strategy'] == 'Total']['Accuracy'].mean()
        total_fdr = project_results[project_results['Strategy'] == 'Total']['FDR'].mean()
        min_accuracy_lines = project_results[project_results['Strategy'] == 'MinLines']['Accuracy'].mean()
        min_fdr_lines = project_results[project_results['Strategy'] == 'MinLines']['FDR'].mean()
        max_accuracy_lines = project_results[project_results['Strategy'] == 'MaxLines']['Accuracy'].mean()
        max_fdr_lines = project_results[project_results['Strategy'] == 'MaxLines']['FDR'].mean()
        mean_accuracy_lines = project_results[project_results['Strategy'] == 'MeanLines']['Accuracy'].mean()
        mean_fdr_lines = project_results[project_results['Strategy'] == 'MeanLines']['FDR'].mean()
        total_accuracy_lines = project_results[project_results['Strategy'] == 'TotalLines']['Accuracy'].mean()
        total_fdr_lines = project_results[project_results['Strategy'] == 'TotalLines']['FDR'].mean()


        accuracy_max.append(max_accuracy)
        fdr_max.append(max_fdr)
        accuracy_min.append(min_accuracy)
        fdr_min.append(min_fdr)
        accuracy_mean.append(mean_accuracy)
        fdr_mean.append(mean_fdr)
        accuracy_total.append(total_accuracy)
        fdr_total.append(total_fdr)
        accuracy_max_lines.append(max_accuracy_lines)
        fdr_max_lines.append(max_fdr_lines)
        accuracy_min_lines.append(min_accuracy_lines)
        fdr_min_lines.append(min_fdr_lines)
        accuracy_mean_lines.append(mean_accuracy_lines)
        fdr_mean_lines.append(mean_fdr_lines)
        accuracy_total_lines.append(total_accuracy_lines)
        fdr_total_lines.append(total_fdr_lines)


        with open(output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([project_name, min_accuracy, min_fdr, max_accuracy, max_fdr, mean_accuracy, mean_fdr, total_accuracy, total_fdr, min_accuracy_lines, min_fdr_lines, max_accuracy_lines, max_fdr_lines, mean_accuracy_lines, mean_fdr_lines, total_accuracy_lines, total_fdr_lines])
            f.close()

    strategies = {
        "Min Accuracy": accuracy_min,
        "Min FDR": fdr_min,
        "Max Accuracy": accuracy_max,
        "Max FDR": fdr_max,
        "Mean Accuracy": accuracy_mean,
        "Mean FDR": fdr_mean,
        "Total Accuracy": accuracy_total,
        "Total FDR": fdr_total,
        "Min Lines Accuracy": accuracy_min_lines,
        "Min Lines FDR": fdr_min_lines,
        "Max Lines Accuracy": accuracy_max_lines,
        "Max Lines FDR": fdr_max_lines,
        "Mean Lines Accuracy": accuracy_mean_lines,
        "Mean Lines FDR": fdr_mean_lines,
        "Total Lines Accuracy": accuracy_total_lines,
        "Total Lines FDR": fdr_total_lines
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
