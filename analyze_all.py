import os
import pandas as pd
import time

projects_path="/home/mdsiam/Desktop/extension/defects4j-repos"
output_path="changes_with_line_fixed_2"
time_path="time_analysis/changes_with_line_fixed_2"

for project in os.listdir(projects_path):
    
    # check whether the project is a directory
    if not os.path.isdir(os.path.join(projects_path, project)):
        continue

    # if output_path does not exist, create it
    if not os.path.exists(os.path.join(output_path, project)):
        os.makedirs(os.path.join(output_path, project))

    # if timepath/project.txt does not exist, create it
    if not os.path.exists(f"{time_path}/{project}.txt"):
        with open(f"{time_path}/{project}.txt", "w") as f:
            f.write("version, time\n")
            f.close()
    # check if the project exist already in output_path
    # if os.path.exists(os.path.join(output_path, project)):
    #     continue
    # iterate over the version1s of the project
    for version in os.listdir(os.path.join(projects_path, project)):
        
        if not os.path.isdir(os.path.join(projects_path, project, version)):
            continue

        if version == "jars":
            continue
        start_time = time.time()

        version_path = os.path.join(projects_path, project, version)

        # if a file with the name version.csv exists, skip it
        

        version_number = int(version[:-1])
        if os.path.exists(f"{output_path}/{project}/{version_number}.csv"):
            print(f"Skipping {project} {version}...")
            continue
        print(f"Analyzing {project} {version_number}...")
        
        command = f"bash head_analyze_change.sh {project} {version_path} {version_number}.csv"
        os.system(command)
        end_time = time.time()
        total_time = end_time - start_time
        with open(f"{time_path}/{project}.txt", "a") as f:
            f.write(f"{version_number}, {total_time}\n")
        # input() 

