# this generates a multi level callgraph of the test code and returns the used classes (all classes over hierarchy levels) in the test code

import os
import re
import csv
import pandas as pd

function_calls_path = "/home/mdsiam/Desktop/extension/Callgraph/cg3"
all_test_cases_path = "../Data/unique_test_cases.csv"
out_dir = "class_invocations"
not_found_dir = "not_found"
test_cases = pd.read_csv(all_test_cases_path)
fault_test_cases_path = "../Data/faults_tests.csv"

def get_test_cases(project, version):
    # print(project, version)
    tcs = test_cases[(test_cases['project'] == project.capitalize()) & (test_cases['version'] == version)]
    return tcs['test_case'].to_list()

assert_methods = [
    "assert", "assertEquals", "assertEqualsNoOrder", "assertArrayEquals", "assertNotEquals", 
    "assertTrue", "assertFalse", "assertNull", "assertNotNull", "assertSame", 
    "assertNotSame", "assertThat", "assertThrows", "fail"
]

def remove_duplicates(input_list):
    return list(dict.fromkeys(input_list))

def format_method_name(input_string):
    # print('input string:',input_string)
    # Extract the class and method names using regular expressions
    match = re.match(r'([a-zA-Z0-9._]+):([^<(]+).*', input_string)
    if match:
        class_name = match.group(1)
        method_name = match.group(2).split('.')[-1]
        return f"{class_name}.{method_name}()"
    else:
        # if input_string.__contains__("<init>"):
        #     # print("init paisi", input_string)
        #     # input()
        # else :
        #     print("init nai", input_string)
        #     # input()

        # Return the original string if the format doesn't match
        return input_string

def get_all_used_classes(method, function_calls, methods, visited=None):
    if visited is None:
        visited = set()
    
    if method in visited:
        return set()
    
    visited.add(method)
    
    used_classes = set(methods.get(method, []))
    
    if method in function_calls:
        for called_method in function_calls[method]:
            used_classes.update(get_all_used_classes(called_method, function_calls, methods, visited))
    
    return used_classes

def extract_invoked_classes():

    for file_name in os.listdir(function_calls_path):
        # file names are of the format: {Project}_{version}_buggy.txt
        project, version, _ = file_name.split("_")
        # print(f"Processing {project}_{version}")
        # skip the Closure project, and Lang 65 for now
        if project == 'Closure':
            continue
        if project == 'Lang' and version == '65':
            continue
        fault_case_df = pd.read_csv(fault_test_cases_path)
        vv = fault_case_df[(fault_case_df['project'] == project) & (fault_case_df['fault_id'] == int(version))]['version'].values[0]
        tcs = get_test_cases(project, vv)
        if not os.path.exists(f"{out_dir}/{project}"):
            os.makedirs(f"{out_dir}/{project}")
        out_file = f"{out_dir}/{project}/{version}.csv"
        with open(os.path.join(function_calls_path, file_name), "r") as file:
            lines = file.readlines()
            lines = remove_duplicates(lines)
            methods = {}
            function_calls = {}

            for line in lines:
                # print('line:',line, end='')
                caller = format_method_name(line.split()[0][2:])[:-2]
                # print('caller:',caller)
                callee = format_method_name(line.split()[1][3:])[:-2]
                # print('callee:',callee)
                # print(caller, callee)
                # input()
                
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
                
                # print(caller, callee)
            

                # for method in assert_methods:
                #     print(method in caller, method in callee)
                #     # input()
                # print(any(method in caller for method in assert_methods) or any(method in callee for method in assert_methods))
                # if the caller or callee contains the assert methods, skip the line
                if any(method in caller for method in assert_methods) or any(method in callee for method in assert_methods):
                    # print('assert method found')
                    continue
                
                if not callee.__contains__("<init>"):
                    if function_calls.get(caller) is None:
                        function_calls[caller] = set()
                    function_calls[caller].add(callee)

                # input()
                # Add callee_class to the caller's list of used classes
                if caller in methods:
                    methods[caller].append(callee_class)
                else:
                    methods[caller] = [callee_class, caller_class] # Include the caller class as well, since we are considering the change proneness of the classes used by the test case as well
            
            # print(function_calls['org.apache.commons.lang.BooleanUtilsTest.test_isFalse_Boolean'])
            
            all_method_classes = {}

            # Iterate through all methods
            for method in methods:
                all_method_classes[method] = get_all_used_classes(method, function_calls, methods)

            # save the list of all used classes for each method in a csv file
            # with open(out_file, 'w') as file:
            #     cc = 0
            #     not_found = []
            #     writer = csv.writer(file)
            #     writer.writerow(["Method", "Used Classes"])
            #     for method in tcs:
            #         if method in all_method_classes:
            #             writer.writerow([method, ", ".join(all_method_classes[method])])
            #         else:
            #             writer.writerow([method, ""])
            #             not_found.append(method)
            #             cc += 1
            #     print(f"{cc} test cases not found in the call graph")
            #     if not os.path.exists(f"{not_found_dir}/{project}"):
            #         os.makedirs(f"{not_found_dir}/{project}")
            #     # save the test cases not found in the call graph
            #     with open(f"{not_found_dir}/{project}/{version}_not_found.txt", "w") as nf:
            #         for method in not_found:
            #             nf.write(f"{method}\n")
            #     print(f"Output saved to {out_file}")
                    
            faulty_methods = fault_case_df[(fault_case_df['project'] == project) & (fault_case_df['fault_id'] == int(version))]['test_case'].unique()
            cc = 0
            not_found = []
            for method in tcs:
                if method in all_method_classes:
                    cc += 1
                else:
                    not_found.append(method)

            if any (method in faulty_methods for method in not_found):
                print(f"Faulty test cases not found in the call graph: {method}, {project}, {version}")

extract_invoked_classes()