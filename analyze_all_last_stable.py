import os
import pandas as pd
import time
# test change
defects4j_projects_path = "/home/mdsiam/Desktop/extension/defects4j/framework/projects"
time_path = "time_analysis/changes_last_stable_with_line_fixed_3"
project_dirs = [
    # {
    #     "project": "Chart",
    #     "dir": "jfreechart"
    # },
    {
        "project": "Csv",
        "dir": "commons-csv"
    },
    {
        "project": "Cli",
        "dir": "commons-cli"
    },
    {
        "project": "Compress",
        "dir": "commons-compress"
    },
    {
        "project": "Closure",
        "dir": "closure-compiler"
    },
    {
        "project": "Codec",
        "dir": "commons-codec"
    },
    {
        "project": "Collections",
        "dir": "commons-collections"
    },
    {
        "project": "Gson",
        "dir": "gson"
    },
    {
        "project": "JacksonCore",
        "dir": "jackson-core"
    },
    {
        "project": "JacksonDatabind",
        "dir": "jackson-databind"
    },
    {
        "project": "JacksonXml",
        "dir": "jackson-dataformat-xml"
    },
    {
        "project": "Jsoup",
        "dir": "jsoup"
    },
    {
        "project": "JxPath",
        "dir": "commons-jxpath"
    },
    {
        "project": "Lang",
        "dir": "lang-d"
    },
    {
        "project": "Math",
        "dir": "lang-d"
    },
    {
        "project": "Mockito",
        "dir": "mockito"
    },
    {
        "project": "Time",
        "dir": "joda-time"
    }
]

for project_dir in project_dirs:
    project = project_dir["project"]
    dir = project_dir["dir"]

    bugs_file = f"{defects4j_projects_path}/{project}/active-bugs.csv"
    bugs_eunmarated_file = f"{defects4j_projects_path}/{project}/active-bugs-with-commit-number.csv"
    df = pd.read_csv(bugs_file)
    df_enumerated = pd.read_csv(bugs_eunmarated_file)
    # sort the dataframe by commit_number and then commit_number_fixed
    df_enumerated = df_enumerated.sort_values(by=["commit_number", "commit_number_fixed"])

    output_dir = f"/home/mdsiam/Desktop/extension/change-defect-relation-analysis/Code/changes_stable_with_line_fixed_3/{project}"
    print(f"Analyzing {project}...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    time_file = f"{time_path}/{project}.txt"
    if not os.path.exists(time_file):
        with open(time_file, "w") as f:
            f.write("version, time\n")
            f.close()
    for index, row in df_enumerated.iterrows():
        current_version = row["current_version"]
        bug_id = row["bug_id"]
        
        # if project != 'Lang' or bug_id != 4:
        #     continue
        # input()
        print(f"Analyzing \t - {current_version}...")
        output_file = f"{output_dir}/{bug_id}.csv"
        start_time = time.time()
        if index == 0:
            os.system(f"bash analyze_changes_with_specific_hash.sh {dir} {current_version} {output_file}")
            
        else:
            last_stable_version = df_enumerated.iloc[index - 1]["fixed_version"]
            if last_stable_version == current_version:
                last_stable_version = df_enumerated.iloc[index - 1]["current_version"]
            os.system(f"bash analyze_changes_with_specific_hash.sh {dir} {last_stable_version} {current_version} {output_file}")
        end_time = time.time()
        total_time = end_time - start_time
        with open(time_file, "a") as f:
            f.write(f"{bug_id}, {total_time}\n")

        # input()