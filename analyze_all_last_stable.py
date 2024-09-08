import os
import pandas as pd

defects4j_projects_path = "/home/mdsiam/Desktop/extension/defects4j/framework/projects"

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
        "dir": "commons-lang"
    },
    {
        "project": "Math",
        "dir": "commons-math"
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
    df = pd.read_csv(bugs_file)
    output_dir = f"/home/mdsiam/Desktop/extension/change-defect-relation-analysis/Code/changes_stable_3/{project}"
    print(f"Analyzing {project}...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for index, row in df.iterrows():
        current_version = row["revision.id.buggy"]
        print(f"Analyzing \t - {current_version}...")
        bug_id = row["bug.id"]
        output_file = f"{output_dir}/{bug_id}.csv"
        
        if index == 0:
            os.system(f"bash analyze_changes_with_specific_hash.sh {dir} {current_version} {output_file}")
            
        else:
            last_stable_version = df.iloc[index - 1]["revision.id.buggy"]
            # if last_stable_version == current_version:
            #     last_stable_version = df.iloc[index - 1]["revision.id.buggy"]
            os.system(f"bash analyze_changes_with_specific_hash.sh {dir} {last_stable_version} {current_version} {output_file}")