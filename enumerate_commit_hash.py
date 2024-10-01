import os
import pandas as pd
import csv

defects4j_projects_path = "/home/mdsiam/Desktop/extension/defects4j/framework/projects"

# projects lang, mockito, time and math do not work, they show the hashes are not available

project_dirs = [
    # {
    #     "project": "Chart",
    #     "dir": "jfreechart"
    # },
    # {
    #     "project": "Csv",
    #     "dir": "commons-csv"
    # },
    # {
    #     "project": "Cli",
    #     "dir": "commons-cli"
    # },
    # {
    #     "project": "Compress",
    #     "dir": "commons-compress"
    # },
    # {
    #     "project": "Closure",
    #     "dir": "closure-compiler"
    # },
    # {
    #     "project": "Codec",
    #     "dir": "commons-codec"
    # },
    # {
    #     "project": "Collections",
    #     "dir": "commons-collections"
    # },
    # {
    #     "project": "Gson",
    #     "dir": "gson"
    # },
    # {
    #     "project": "JacksonCore",
    #     "dir": "jackson-core"
    # },
    # {
    #     "project": "JacksonDatabind",
    #     "dir": "jackson-databind"
    # },
    # {
    #     "project": "JacksonXml",
    #     "dir": "jackson-dataformat-xml"
    # },
    # {
    #     "project": "Jsoup",
    #     "dir": "jsoup"
    # },
    # {
    #     "project": "JxPath",
    #     "dir": "commons-jxpath"
    # },
    {
        "project": "Lang",
        "dir": "commons-lang"
    },
    # {
    #     "project": "Math",
    #     "dir": "commons-math"
    # },
    # {
    #     "project": "Mockito",
    #     "dir": "mockito"
    # },
    # {
    #     "project": "Time",
    #     "dir": "joda-time"
    # }
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
        print(f"Analyzing \t - {bug_id}...")
        
        # cd to ../Projects/{project}, checkout to current version and get the total number of commits from HEAD to current version
        os.system(f"cd ../Projects/{dir} && git checkout {current_version} && git rev-list HEAD --count > /tmp/commit_number.txt")
        with open("/tmp/commit_number.txt", "r") as f:
            commit_number = int(f.read())
        os.system("rm /tmp/commit_number.txt")

        # cd to ../Projects/{project}, checkout to fixed version and get the total number of commits from HEAD to fixed version
        os.system(f"cd ../Projects/{dir} && git checkout {fixed_version} && git rev-list HEAD --count > /tmp/commit_number.txt")
        with open("/tmp/commit_number.txt", "r") as f:
            commit_number_fixed = int(f.read())
        os.system("rm /tmp/commit_number.txt")

        # if the output file doesn't exist, create it
        if not os.path.exists(output_path):
            with open(output_path, "w") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["bug_id", "current_version", "commit_number", "fixed_version", "commit_number_fixed"])
                f.close()
        # write the commit number to the output file
        with open(output_path, "a") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([bug_id, current_version, commit_number, fixed_version, commit_number_fixed])
            f.close()

        # input("Press Enter to continue...")
