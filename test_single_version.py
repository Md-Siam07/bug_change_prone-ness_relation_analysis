import os
import pandas as pd
import csv
import json

test_cases_change_proneness_dir = "testcase_change_proneness_stable"
faulty_testcases_dir = "/home/mdsiam/Desktop/extension/ATM_artifacts_(1)/Data/faults_tests.csv"

columns = ['Project', 'Version', 'Strategy', 'Budget', 'SelectedTestCases']
versions = [2]
projects = ['Gson']
for project in projects:
    fault_cases = pd.read_csv(faulty_testcases_dir)
    fault_cases = fault_cases[fault_cases['project'] == project.capitalize()]
    fault_cases = fault_cases[fault_cases['fault_id'].isin(versions)]
    project_path = os.path.join(test_cases_change_proneness_dir, project)
    print(fault_cases)
    # versions = [int(file.split('.')[0]) for file in os.listdir(project_path)]
    # versions.sort()
    
    for version in versions:
        
        testcase_change_proneness_values = pd.read_csv(f"{project_path}/{version}.csv")

        values_sorted_total = testcase_change_proneness_values.sort_values(by='SumChangeProneness', ascending=False)
        values_sorted_mean = testcase_change_proneness_values.sort_values(by='AvgChangeProneness', ascending=False)
        values_sorted_max = testcase_change_proneness_values.sort_values(by='MaxChangeProneness', ascending=False)
        values_sorted_min = testcase_change_proneness_values.sort_values(by='MinChangeProneness', ascending=False)

        for budget in 25, 50, 75:
            number_of_testcases = int(len(testcase_change_proneness_values) * budget / 100)
            
            selected_testcases_total = values_sorted_total.head(number_of_testcases)
            selected_testcases_mean = values_sorted_mean.head(number_of_testcases)
            selected_testcases_max = values_sorted_max.head(number_of_testcases)
            selected_testcases_min = values_sorted_min.head(number_of_testcases)
            
            print(selected_testcases_max.tail(100))
            selected_testcases = selected_testcases_total['TestCase'].to_list()
            accuracy = len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) / len(fault_cases['test_case'].to_list())
            fdr = 0 if len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) == 0 else 1
            print(project, version, 'total', accuracy, fdr)

            selected_testcases = selected_testcases_mean['TestCase'].to_list()
            accuracy = len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) / len(fault_cases['test_case'].to_list())
            
            # print the index of com.google.gson.functional.DefaultTypeAdaptersTest.testJsonElementTypeMismatch in maxchanges

            fdr = 0 if len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) == 0 else 1
            print(project, version, 'mean', accuracy, fdr)

            selected_testcases = selected_testcases_max['TestCase'].to_list()
            accuracy = len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) / len(fault_cases['test_case'].to_list())
            fdr = 0 if len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) == 0 else 1
            print(project, version, 'max', accuracy, fdr)

            selected_testcases = selected_testcases_min['TestCase'].to_list()
            accuracy = len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) / len(fault_cases['test_case'].to_list())
            fdr = 0 if len(set(selected_testcases).intersection(fault_cases['test_case'].to_list())) == 0 else 1
            print(project, version, 'min', accuracy, fdr)