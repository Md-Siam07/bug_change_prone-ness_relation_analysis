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
class_invocation_path = "class_invocations"

def string_to_list(class_string):
    if pd.isna(class_string):
        return []
    return [cls.strip() for cls in class_string.split(',')]

for project in os.listdir(class_invocation_path):

    if project == 'Chart':
        continue

    versions = [int(file.split('.')[0]) for file in os.listdir(os.path.join(class_invocation_path, project))]
    versions.sort()
    
    for version in versions:
        print(project, version)
        
        tcs = pd.read_csv(f"{class_invocation_path}/{project}/{version}.csv")
        tcs['Used Classes'] = tcs['Used Classes'].apply(string_to_list)
        
        # open the change_proneness file
        change_proneness_df = pd.read_csv(f"{change_dir}/{project}/{version}.csv")
        change_proneness_df['Ratio']=change_proneness_df['Changes']/change_proneness_df['TotalCommits']
        change_proneness_df['LinesRatio'] = (change_proneness_df['Insertions'] + change_proneness_df['Deletions'])/change_proneness_df['TotalCommits']
        results = []
        for index, row in tcs.iterrows():
            tc = row['Method']
            used_classes = row['Used Classes']
            # print(tc, used_classes)

            # get the change proneness of the used classes
            change_proneness_values = change_proneness_df[change_proneness_df['ClassName'].isin(used_classes)]
            # print(used_classes_change_proneness)

            output_file_path = f"{output_dir}/{project}/{version}.csv"
            if not os.path.exists(f"{output_dir}/{project}"):
                os.makedirs(f"{output_dir}/{project}")
            
            # if output file already exists, skip 
            if os.path.exists(output_file_path):
                continue
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
            continue
        # Sort the DataFrame by 'SumChangeProneness'
        results_df = results_df.sort_values(by='Sum', ascending=False)

        # Save the sorted DataFrame to a CSV file
        

        results_df.to_csv(output_file_path, index=False)