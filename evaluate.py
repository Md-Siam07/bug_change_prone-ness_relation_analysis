import os
import pandas as pd
import json
import csv

results_dir = "results/greedy_change_proneness_stable"
output_dir = "accuracy/greedy_change_proneness_stable_2"
faulty_testcases_dir = "/home/mdsiam/Desktop/extension/ATM_artifacts_(1)/Data/faults_tests.csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for budget in os.listdir(results_dir):
    
    budget_dir = os.path.join(results_dir, budget)
    
    for project in os.listdir(budget_dir):
        project_name = project.split('.')[0]
        project_results = pd.read_csv(f"{budget_dir}/{project}")

        for version in project_results['Version'].unique():
            version_results = project_results[project_results['Version'] == version]
            faulty_testcases = pd.read_csv(faulty_testcases_dir)
            faulty_testcases = faulty_testcases[(faulty_testcases['project'] == project_name.capitalize()) & (faulty_testcases['fault_id'] == version)]

            faulty_testcases_list = faulty_testcases['test_case'].to_list()

            for strategy in ['Total', 'Mean', 'Max', 'Min']:
                
                strategy_results = version_results[version_results['Strategy'] == strategy]

                selected_testcases = json.loads(strategy_results['SelectedTestCases'].iloc[0])
                accuracy = len(set(selected_testcases).intersection(faulty_testcases_list)) / len(faulty_testcases_list)
                fdr = 0 if len(set(selected_testcases).intersection(faulty_testcases_list)) == 0 else 1
                # if(project_name == 'Cli' and version ==32):
                #     print(project, version, strategy, accuracy, fdr)
                #     print(faulty_testcases_list)
                # print(os.path.exists(f"{output_dir}/{budget}"), f"{output_dir}/{budget}")
                if not os.path.exists(f"{output_dir}/{budget}"):
                    # print(f"Creating directory: {output_dir}/{budget}")
                    os.makedirs(f"{output_dir}/{budget}")

                if not os.path.exists(f"{output_dir}/{budget}/{project}"):
                    with open(f"{output_dir}/{budget}/{project}", "w") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Version", "Strategy", "Accuracy", "FDR"])
                        writer.writerow([version, strategy, accuracy, fdr])
                        file.close()
                else:
                    with open(f"{output_dir}/{budget}/{project}", "a") as file:
                        writer = csv.writer(file)
                        writer.writerow([version, strategy, accuracy, fdr])
                        file.close()

                

