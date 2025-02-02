#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 <project-directory> [<start-hash>] <end-hash> <output-path>"
    exit 1
fi

# Assign arguments to variables
project_dir=$1

# Check if start-hash is provided, if not set a default (e.g., the first commit)
if [ "$#" -eq 4 ]; then
    start_hash=$2
    end_hash=$3
    output_path=$4
else
    start_hash=$(git -C "../Projects/$project_dir" rev-list --max-parents=0 HEAD) # First commit
    echo "Start hash: $start_hash"
    end_hash=$2
    output_path=$3
fi


csv_file=$output_path

# Check if the specified project directory exists
if [ ! -d "$output_path" ]; then
    
    # If the directory does not exist, create it (the last portion of / is the file name)
    touch $output_path
fi

# Change to the specified project directory
if ! cd "../Projects/$project_dir"; then
    echo "Error: Unable to change directory to $project_dir"
    exit 1
fi

# Get the list of files changed between the two commits
changed_files=$(git log --name-only -l0 --pretty=format: $start_hash..$end_hash | grep -v '^$' | sort | uniq)

echo "ClassName,Changes,TotalCommits,Insertions,Deletions" >> "$csv_file"

if [ $? -ne 0 ]; then
    echo "Error: Unable to create CSV file at $csv_file"
    exit 1
fi

calculate_insertions_deletions() {
    local file=$1
    local start_commit=$2
    local end_commit=$3
    
    # Use git log with --numstat to capture file-specific changes
    local output=$(git log --numstat -l0 $start_commit..$end_commit -- "$file")
    local total_insertions=0
    local total_deletions=0
    
    # Loop through each line in the output to accumulate insertions and deletions
    while IFS= read -r line; do
        if [[ $line =~ ^[0-9]+[[:space:]]+[0-9]+[[:space:]]+$file ]]; then
            insertions=$(echo $line | awk '{print $1}')
            deletions=$(echo $line | awk '{print $2}')
            total_insertions=$((total_insertions + insertions))
            total_deletions=$((total_deletions + deletions))
        fi
    done <<< "$output"
    
    # Return insertions and deletions
    echo "$total_insertions $total_deletions"
}

# Analyze each file
for file in $changed_files; do
    # Check if the file is a Java file
    if [[ $file == *.java ]]; then
        # Extract class name (remove path and .java extension)
        class_name=$(basename "$file" .java)
        
        # If the class name contains slashes (nested classes), take the last part
        class_name=${class_name##*/}
        
        # creation_hash=$(git log --find-renames --diff-filter=A -- "$file" | head -n 1 | cut -d ' ' -f 2)
        creation_hash=$(git log --follow --format="%H" -- "$file" | tail -n 1)
        changes=$(git rev-list --count $start_hash..$end_hash -- "$file")
        total=$(git rev-list --count $creation_hash..$end_hash)
        between_hashes=$(git rev-list --count $start_hash..$end_hash)
        showstat=$(git diff --name-status $start_hash..$end_hash -- "$file")
        # echo $file
        # Get the diff stat
        ins_del=$(calculate_insertions_deletions "$file" "$creation_hash" "HEAD")
        insertions=$(echo $ins_del | cut -d' ' -f1)
        deletions=$(echo $ins_del | cut -d' ' -f2)
        insertions=${insertions:-0}
        deletions=${deletions:-0}

        
        # total should be the minimum between the total number of commits and the number of commits between the two hashes
        if [ $total -gt $between_hashes ]; then
            total=$between_hashes
        fi

        # Append to CSV file
        echo "$class_name,$changes,$total,$insertions,$deletions" >> "$csv_file"
        
    fi
done
