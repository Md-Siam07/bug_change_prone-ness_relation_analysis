import pandas as pd
import numpy as np
import os
import re
import json

change_dir = "accumulated_changes_stable_with_line_fixed_4"
function_call_path = "/home/mdsiam/Desktop/extension/Callgraph/cg2"
all_test_cases_path = "/home/mdsiam/Desktop/extension/ATM_artifacts_(1)/Data/unique_test_cases.csv"
output_dir = "test_case_change_proneness_stable_with_line_fixed_4"

test_cases = pd.read_csv(all_test_cases_path)

def get_test_cases(project, version):
    print(project, version)
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

def calculate_testcase_change_proneness(change_proneness_df, version, project):
    
    output_file_path = f"{output_dir}/{project}/{version}.csv"
    
    #  return if the file already exists
    if os.path.exists(output_file_path):
        return
    
    if not os.path.exists(f"{output_dir}/{project}"):
        os.makedirs(f"{output_dir}/{project}")

    if not os.path.exists(f"{function_call_path}/{project.lower()}_{version}_buggy.txt"):
        print(f"File not found: {function_call_path}/{project.lower()}_{version}_buggy.txt")
        return

    with open(f"{function_call_path}/{project.lower()}_{version}_buggy.txt", "r") as file:
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
            methods[caller] = [caller_class, callee_class]
    print(methods)
    # Get test cases for the given project and version
    tcs = get_test_cases(project, version)

    # Prepare a DataFrame to store the results
    results = []
    # print(tcs)
    for tc in tcs:
        if tc not in methods:
            continue
        used_classes = methods[tc]
        print(f"Test case: {tc}")
        print(f"Used classes: {used_classes}")
        change_proneness_values = change_proneness_df[change_proneness_df['ClassName'].isin(used_classes)]
        
        # Calculate change proneness metrics
        max_cp = change_proneness_values['Ratio'].max()
        avg_cp = change_proneness_values['Ratio'].mean()
        min_cp = change_proneness_values['Ratio'].min()
        sum_cp = change_proneness_values['Ratio'].sum()

        # Store the results in a list
        results.append({
            'TestCase': tc,
            'UsedClasses': json.dumps(used_classes),
            # change proneness values as a JSON string
            'ChangePronenessValues': change_proneness_values.to_json(orient='records'),
            'MaxChangeProneness': max_cp,
            'AvgChangeProneness': avg_cp,
            'MinChangeProneness': min_cp,
            'SumChangeProneness': sum_cp
        })

    # Convert the list to a DataFrame
    results_df = pd.DataFrame(results)
    print(results_df)
    if results_df.empty:
        return
    # Sort the DataFrame by 'SumChangeProneness'
    results_df = results_df.sort_values(by='SumChangeProneness', ascending=False)

    # Save the sorted DataFrame to a CSV file
    

    results_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    
    for project in os.listdir(change_dir):
        project_path = os.path.join(change_dir, project)
        versions = [int(file.split('.')[0]) for file in os.listdir(project_path)]
        versions.sort()
        
        for version in versions:
            change_proneness_df = pd.read_csv(f"{project_path}/{version}.csv")
            change_proneness_df['Ratio']=change_proneness_df['Changes']/change_proneness_df['TotalCommits']
            calculate_testcase_change_proneness(change_proneness_df, version, project)
            input("Press Enter to continue...")