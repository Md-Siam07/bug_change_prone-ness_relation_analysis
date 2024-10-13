import pandas as pd
import numpy as np
import os
import re
from scipy import stats
import json

change_dir = "accumulated_changes_stable_with_line_fixed_4"
function_call_path = "/home/mdsiam/Desktop/extension/Callgraph/cg2"
all_test_cases_path = "../Data/unique_test_cases.csv"
output_dir = f"testcase_change_proneness_{change_dir.replace('accumulated_changes_', '')}"
fault_test_cases_path = "../Data/faults_tests.csv"

test_cases = pd.read_csv(all_test_cases_path)

def get_test_cases(project, version):
    # print(project, version)
    tcs = test_cases[(test_cases['project'] == project.capitalize()) & (test_cases['version'] == version)]
    return tcs['test_case'].to_list()


def format_method_name(input_string):
    # Extract the class and method names using regular expressions
    match = re.match(r'([a-zA-Z0-9._]+):([^<(]+).*', input_string)
    if match:
        class_name = match.group(1)
        method_name = match.group(2).split('.')[-1]
        return f"{class_name}.{method_name}()"
    else:
        # Return the original string if the format doesn't match
        return input_string

def remove_duplicates(input_list):
    return list(dict.fromkeys(input_list))

def calculate_testcase_change_proneness(change_proneness_df, version, project, faulty_version):
    
    output_file_path = f"{output_dir}/{project}/{version}.csv"
    
    #  return if the file already exists
    # if os.path.exists(output_file_path):
    #     return
    
    if not os.path.exists(f"{output_dir}/{project}"):
        os.makedirs(f"{output_dir}/{project}")

    cg_file_path = f"{function_call_path}/{project.lower()}_{faulty_version}_buggy.txt"

    if not os.path.exists(cg_file_path):
        print(f"File not found: {cg_file_path}")
        return

    with open(cg_file_path, "r") as file:
        lines = file.readlines()
        lines = remove_duplicates(lines)

    methods = {}

    for line in lines:
        caller = format_method_name(line.split()[0][2:])[:-2]
        callee = format_method_name(line.split()[1][3:])[:-2]
        
        try:
            caller_class = caller.split('.')[-2]
        except:
            continue

        if caller.__contains__(":"):
            caller = caller.split(":")[0]
            caller_class = caller.split('.')[-1]

        try:
            callee_class = callee.split('.')[-2]
        except:
            continue

        if callee.__contains__(":"):
            callee = callee.split(":")[0]
            callee_class = callee.split('.')[-1]

        call_type = line.split()[1][1]
        is_class_call = format_method_name(line.split()[0][0]) == 'C'
        
        if call_type == 'D' or is_class_call:  # Direct call or object instantiation
            continue
        
        # Add callee_class to the caller's list of used classes
        if caller in methods:
            methods[caller].append(callee_class)
        else:
            methods[caller] = [callee_class, caller_class] # Include the caller class as well, since we are considering the change proneness of the classes used by the test case as well

    # Get test cases for the given project and version
    tcs = get_test_cases(project, version)
    # print the union of the test cases and the methods
    # print(len(set(tcs).intersection(methods.keys())))
    # Prepare a DataFrame to store the results
    results = []
    # print(methods)
    for tc in tcs:
        # print(tc)
        if tc not in methods:
            continue
        used_classes = methods[tc]
        # print(tc, used_classes)
        change_proneness_values = change_proneness_df[change_proneness_df['ClassName'].isin(used_classes)]
        # print(change_proneness_values)
        # Calculate change proneness metrics
        max_cp = change_proneness_values['Ratio'].max()
        avg_cp = change_proneness_values['Ratio'].mean()
        min_cp = change_proneness_values['Ratio'].min()
        sum_cp = change_proneness_values['Ratio'].sum()
        ratio_column = change_proneness_values['Ratio']
        # print(tc, used_classes)
        # Filter out zero or negative values
        ratio_column_non_zero = change_proneness_values['Ratio'][change_proneness_values['Ratio'] > 0]

        # if the ratio_column is empty, skip the test case
        # if ratio_column_non_zero.empty:
        #     print(tc, used_classes)
        #     input("Press Enter to continue...")

        # Calculate harmonic mean and geometric mean without NaN
        harmonic_mean = stats.hmean(ratio_column_non_zero)
        # print(harmonic_mean, ratio_column_non_zero)
        geometric_mean = stats.gmean(ratio_column_non_zero)
        standard_deviation = np.std(ratio_column_non_zero)
        min_max_normalization = (ratio_column - ratio_column.min()) / (ratio_column.max() - ratio_column.min())

        # Calculate the sum of the lines ratio
        sum_lines_ratio = change_proneness_values['LinesRatio'].sum()
        avg_lines_ratio = change_proneness_values['LinesRatio'].mean()
        max_lines_ratio = change_proneness_values['LinesRatio'].max()
        min_lines_ratio = change_proneness_values['LinesRatio'].min()

        lines_ratio_column = change_proneness_values['LinesRatio']
        lines_ratio_column_non_zero = lines_ratio_column[lines_ratio_column > 0]

        # Calculate harmonic mean and geometric mean without NaN
        harmonic_mean_lines_ratio = stats.hmean(lines_ratio_column_non_zero)
        geometric_mean_lines_ratio = stats.gmean(lines_ratio_column_non_zero)
        standard_deviation_lines_ratio = np.std(lines_ratio_column_non_zero)
        # min_max_normalization_lines_ratio = (lines_ratio_column - lines_ratio_column.min()) / (lines_ratio_column.max() - lines_ratio_column.min())

        # Store the results in a list
        results.append({
            'TestCase': tc,
            'Max': max_cp,
            'Avg': avg_cp,
            'Min': min_cp,
            'Sum': sum_cp,
            'HarmonicMean': harmonic_mean,
            'GeometricMean': geometric_mean,
            'StandardDeviation': standard_deviation,
            # 'MinMaxNormalization': min_max_normalization.to_list(),
            'MaxLinesRatio': max_lines_ratio,
            'AvgLinesRatio': avg_lines_ratio,
            'MinLinesRatio': min_lines_ratio,
            'SumLinesRatio': sum_lines_ratio,
            'HarmonicMeanLinesRatio': harmonic_mean_lines_ratio,
            'GeometricMeanLinesRatio': geometric_mean_lines_ratio,
            'StandardDeviationLinesRatio': standard_deviation_lines_ratio,
            'used_classes': json.dumps(used_classes),
            'changeProneness': json.dumps(change_proneness_values['Ratio'].to_list()),
            'linesRatio': json.dumps(change_proneness_values['LinesRatio'].to_list()),
            # 'MinMaxNormalizationLinesRatio': min_max_normalization_lines_ratio.to_list()
        })

    # Convert the list to a DataFrame
    results_df = pd.DataFrame(results)

    if results_df.empty:
        return
    # Sort the DataFrame by 'SumChangeProneness'
    results_df = results_df.sort_values(by='Sum', ascending=False)

    # Save the sorted DataFrame to a CSV file
    

    results_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    
    for project in os.listdir(change_dir):
        project_path = os.path.join(change_dir, project)
        versions = [int(file.split('.')[0]) for file in os.listdir(project_path)]
        versions.sort()
        
        for version in versions:
            # if not (project == "math" and version == 1):
            #     continue
            fault_case_df = pd.read_csv(fault_test_cases_path)
            faulty_version = fault_case_df[(fault_case_df['project'] == project) & (fault_case_df['version'] == version)]['fault_id'].values[0]
            print(f"Calculating change proneness for {project} {version} (faulty version: {faulty_version})")
            # input(f"Press Enter to continue...")
            change_proneness_df = pd.read_csv(f"{project_path}/{faulty_version}.csv")
            change_proneness_df['Ratio']=change_proneness_df['Changes']/change_proneness_df['TotalCommits']
            change_proneness_df['LinesRatio'] = (change_proneness_df['Insertions'] + change_proneness_df['Deletions'])/change_proneness_df['TotalCommits']
            calculate_testcase_change_proneness(change_proneness_df, version, project, faulty_version)
            input("Press Enter to continue...")