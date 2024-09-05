import os
import pandas as pd

projects_path="/home/mdsiam/Desktop/extension/defects4j-repos"

for project in os.listdir(projects_path):
    
    # check whether the project is a directory
    if not os.path.isdir(os.path.join(projects_path, project)):
        continue

    # iterate over the versions of the project
    for version in os.listdir(os.path.join(projects_path, project)):
        
        if not os.path.isdir(os.path.join(projects_path, project, version)):
            continue

        if version == "jars":
            continue
        
        version_path = os.path.join(projects_path, project, version)
        version_number = int(version[:-1])
        
        command = f"bash head_analyze_change.sh {project} {version_path} {version_number}.csv"
        os.system(command)

