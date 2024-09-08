#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <project_name> <project_path> <output-path>"
    exit 1
fi

# project_dir=$1
project_name=$1
original_dir=$(pwd)
project_path=$2
output_path=$3
csv_file="$original_dir/changes_with_line_full_file_name/$project_name/$output_path"

# If the project directory doesn't exist, create it
if [ ! -d "changes_with_line_full_file_name/$project_name" ]; then
    echo "Creating directory $project_name"
    if ! mkdir -p "changes_with_line_full_file_name/$project_name"; then
        echo "Error: Unable to create directory $project_name"
        exit 1
    fi
fi

# Change to the specified project directory
if ! cd "$project_path"; then
    echo "Error: Unable to change directory to $project_path"
    exit 1
fi

# Get the start hash (the first commit)
start_hash=$(git log --pretty=format:%H --reverse | head -n 1)
echo "start hash: $start_hash"

# Get the list of files changed between the two commits
changed_files=$(git log --name-only --pretty=format: $start_hash..HEAD | grep -v '^$' | sort | uniq)

# Create the CSV file
echo "ClassName,Changes,TotalCommits,Insertions,Deletions" >> "$csv_file"

if [ $? -ne 0 ]; then
    echo "Error: Unable to create CSV file at $csv_file"
    exit 1
fi

echo "CSV file created at: $csv_file"

# Analyze each file
for file in $changed_files; do
    # Check if the file is a Java file
    if [[ $file == *.java ]]; then
        # echo "Processing $file"
        # Extract class name (remove path and .java extension)
        class_name=$file
        
        # # If the class name contains slashes (nested classes), take the last part
        # class_name=${class_name##*/}
        
        creation_hash=$(git log --find-renames --diff-filter=A -- "$file" | head -n 1 | cut -d ' ' -f 2)
        changes=$(git rev-list --count $start_hash..HEAD -- "$file")
        total=$(git rev-list --count $creation_hash..HEAD)
        showstat=$(git diff --name-status $creation_hash..HEAD -- "$file")
        # echo $file
        # Get the diff stat
        stat_output=$(git diff --stat $creation_hash..HEAD -- "$file")
        # echo "stat_output: $stat_output"
        # Extract the number of insertions
        insertions=$(echo "$stat_output" | grep -o '[0-9]* insertion' | awk '{print $1}')

        # Extract the number of deletions
        deletions=$(echo "$stat_output" | grep -o '[0-9]* deletion' | awk '{print $1}')

        # Handle cases where no insertions or deletions were found
        insertions=${insertions:-0}
        deletions=${deletions:-0}

        # Append to CSV file
        echo "$class_name,$changes,$total,$insertions,$deletions" >> "$csv_file"
        
        # echo "$file changed $changes times in $total commits"
    fi
done
