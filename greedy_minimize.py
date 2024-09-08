import os
import pandas as pd
import csv
import json

test_cases_change_proneness_dir = "testcase_change_proneness_stable_with_previous_stable"

columns = ['Project', 'Version', 'Strategy', 'Budget', 'SelectedTestCases']

for project in os.listdir(test_cases_change_proneness_dir):
    project_path = os.path.join(test_cases_change_proneness_dir, project)
    versions = [int(file.split('.')[0]) for file in os.listdir(project_path)]
    versions.sort()
    
    for version in versions:
        
        testcase_change_proneness_values = pd.read_csv(f"{project_path}/{version}.csv")

        values_sorted_total = testcase_change_proneness_values.sort_values(by='SumChangeProneness', ascending=False)
        values_sorted_mean = testcase_change_proneness_values.sort_values(by='AvgChangeProneness', ascending=False)
        values_sorted_max = testcase_change_proneness_values.sort_values(by='MaxChangeProneness', ascending=False)
        values_sorted_min = testcase_change_proneness_values.sort_values(by='MinChangeProneness', ascending=False)
        # MaxLinesRatio,AvgLinesRatio,MinLinesRatio,SumLinesRatio
        values_sorted_total_lines = testcase_change_proneness_values.sort_values(by='SumLinesRatio', ascending=False)
        values_sorted_mean_lines = testcase_change_proneness_values.sort_values(by='AvgLinesRatio', ascending=False)
        values_sorted_max_lines = testcase_change_proneness_values.sort_values(by='MaxLinesRatio', ascending=False)
        values_sorted_min_lines = testcase_change_proneness_values.sort_values(by='MinLinesRatio', ascending=False)

        for budget in 25, 50, 75:
            number_of_testcases = int(len(testcase_change_proneness_values) * budget / 100)
            selected_testcases_total = values_sorted_total.head(number_of_testcases)
            selected_testcases_mean = values_sorted_mean.head(number_of_testcases)
            selected_testcases_max = values_sorted_max.head(number_of_testcases)
            selected_testcases_min = values_sorted_min.head(number_of_testcases)
            selected_testcases_total_lines = values_sorted_total_lines.head(number_of_testcases)
            selected_testcases_mean_lines = values_sorted_mean_lines.head(number_of_testcases)
            selected_testcases_max_lines = values_sorted_max_lines.head(number_of_testcases)
            selected_testcases_min_lines = values_sorted_min_lines.head(number_of_testcases)

            output_dir = f"results/greedy_{test_cases_change_proneness_dir.replace('testcase_change_proneness_','')}/{budget}"
            output_file = f"{output_dir}/{project}.csv"
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # crate a file named upon project if it doesn't exist
            if not os.path.exists(output_file):
                file = open(output_file, 'w')
                writer = csv.writer(file)
                writer.writerow(columns)
                file.close()
            
            with open(output_file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([project, version, 'Total', budget, json.dumps(selected_testcases_total['TestCase'].tolist())])
                writer.writerow([project, version, 'Mean', budget, json.dumps(selected_testcases_mean['TestCase'].tolist())])
                writer.writerow([project, version, 'Max', budget, json.dumps(selected_testcases_max['TestCase'].tolist())])
                writer.writerow([project, version, 'Min', budget, json.dumps(selected_testcases_min['TestCase'].tolist())])
                writer.writerow([project, version, 'TotalLines', budget, json.dumps(selected_testcases_total_lines['TestCase'].tolist())])
                writer.writerow([project, version, 'MeanLines', budget, json.dumps(selected_testcases_mean_lines['TestCase'].tolist())])
                writer.writerow([project, version, 'MaxLines', budget, json.dumps(selected_testcases_max_lines['TestCase'].tolist())])
                writer.writerow([project, version, 'MinLines', budget, json.dumps(selected_testcases_min_lines['TestCase'].tolist())])
                f.close()
            

                
