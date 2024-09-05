import pandas as pd
import os

def post_process(file_path, output_path):
    df = pd.read_csv(file_path)
    df['Changes'] = df['Changes'].astype(int)
    df['TotalCommits'] = df['TotalCommits'].astype(int)
    # sum the Changes for each ClassName and max the TotalCommits
    df = df.groupby('ClassName').agg({'Changes': 'sum', 'TotalCommits': 'max'}).reset_index()

    # if total commits is less than or equal to 5, remove the row
    # df = df[df['TotalCommits'] > 5]

    # remove the rows with 0 Changes
    df = df[df['Changes'] > 0]

    # sort by Changes and TotalCommits ratio
    df['Ratio'] = df['Changes'] / df['TotalCommits']
    df = df.sort_values(by='Ratio', ascending=False)
    df.drop(columns=['Ratio'], inplace=True)
    df.to_csv(output_path, index=False)

changes_dir = "changes_stable"

for project in os.listdir(changes_dir):
    project_path = os.path.join(changes_dir, project)
    
    # get the versions from existing csv files, eg. 1.csv, 2.csv
    versions = [int(file.split('.')[0]) for file in os.listdir(project_path)]
    versions.sort()

    # if project path doesnt exist, create it
    if not os.path.exists(f"accumulated_changes_stable/{project}"):
        os.makedirs(f"accumulated_changes_stable/{project}")

    for version in versions:
        post_process(f"{project_path}/{version}.csv", f"accumulated_changes_stable/{project}/{version}.csv")

# post_process('commons-csv/2.csv', "commons-csv/2.csv")