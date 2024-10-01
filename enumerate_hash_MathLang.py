import os
import pandas as pd
import csv

defects4j_projects_path = "/home/mdsiam/Desktop/extension/defects4j/framework/projects"
defects4j_repos_path = "/home/mdsiam/Desktop/extension/defects4j-repos"
# projects lang, mockito, time and math do not work, they show the hashes are not available

project_dirs = [
    {
        "project": "Lang",
        "dir": "commons-lang"
    },
    {
        "project": "Math",
        "dir": "commons-math"
    }
]

for project_dir in project_dirs:
    project = project_dir["project"]
    dir = project_dir["dir"]

    bugs_file = f"{defects4j_projects_path}/{project}/active-bugs.csv"
    df = pd.read_csv(bugs_file)
    output_path = f"{defects4j_projects_path}/{project}/active-bugs-with-commit-number.csv"
    print(f"Analyzing {project}...")
    
    for index, row in df.iterrows():
        current_version = row["revision.id.buggy"]
        fixed_version = row["revision.id.fixed"]
        bug_id = row["bug.id"]
        project_path = os.path.join(defects4j_repos_path, project, '1b')
        print(f"Analyzing \t - {bug_id}...")

        # checkout to current version and get the commit hash
        os.system(f"cd {project_path} && git checkout {current_version} &&  git rev-list HEAD --count > /tmp/commit_hash.txt")
        with open("/tmp/commit_hash.txt", "r") as f:
            commit_hash = int(f.read())
        os.system("rm /tmp/commit_hash.txt")

        # checlout to fixed version and get the commit hash
        os.system(f"cd {project_path} && git checkout {fixed_version} &&  git rev-list HEAD --count > /tmp/commit_hash.txt")
        with open("/tmp/commit_hash.txt", "r") as f:
            commit_hash_fixed = int(f.read())
        os.system("rm /tmp/commit_hash.txt")

        # if the output file doesn't exist, create it
        if not os.path.exists(output_path):
            with open(output_path, "w") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["bug_id", "current_version", "commit_hash", "fixed_version", "commit_hash_fixed"])
                f.close()
        # write the commit number to the output file
        with open(output_path, "a") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([bug_id, current_version, commit_hash, fixed_version, commit_hash_fixed])
            f.close()

