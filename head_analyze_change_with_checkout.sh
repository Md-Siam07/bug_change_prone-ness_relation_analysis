# #!/bin/bash

# # Check if the correct number of arguments is provided
# if [ "$#" -ne 3 ]; then
#     echo "Usage: $0 <project_name> <project_path> <output-path>"
#     exit 1
# fi

# # project_dir=$1
# project_name=$1
# original_dir=$(pwd)
# project_path=$2
# output_path=$3
# csv_file="$original_dir/changes_with_line/$project_name/$output_path"

# # If the project directory doesn't exist, create it
# if [ ! -d "changes_with_line/$project_name" ]; then
#     echo "Creating directory $project_name"
#     if ! mkdir -p "changes_with_line/$project_name"; then
#         echo "Error: Unable to create directory $project_name"
#         exit 1
#     fi
# fi

# # Change to the specified project directory
# if ! cd "$project_path"; then
#     echo "Error: Unable to change directory to $project_path"
#     exit 1
# fi

# # Get the start hash (the first commit)
# start_hash=$(git log --pretty=format:%H --reverse | head -n 1)
# echo "start hash: $start_hash"

# # Get the list of files changed between the two commits
# changed_files=$(git log --name-only --pretty=format: $start_hash..HEAD | grep -v '^$' | sort | uniq)

# # Create the CSV file
# echo "ClassName,Changes,TotalCommits,Insertions,Deletions" >> "$csv_file"

# if [ $? -ne 0 ]; then
#     echo "Error: Unable to create CSV file at $csv_file"
#     exit 1
# fi

# echo "CSV file created at: $csv_file"

# # Analyze each file
# for file in $changed_files; do
#     # Check if the file is a Java file
#     if [[ $file == *.java ]]; then
#         # echo "Processing $file"
#         # Extract class name (remove path and .java extension)
#         class_name=$(basename "$file" .java)
        
#         # If the class name contains slashes (nested classes), take the last part
#         class_name=${class_name##*/}
        
#         creation_hash=$(git log --find-renames --diff-filter=A -- "$file" | head -n 1 | cut -d ' ' -f 2)
#         changes=$(git rev-list --count $start_hash..HEAD -- "$file")
#         total=$(git rev-list --count $creation_hash..HEAD)
#         showstat=$(git diff --name-status $creation_hash..HEAD -- "$file")
#         # echo $file
#         # Get the diff stat
#         stat_output=$(git diff --stat $creation_hash..HEAD -- "$file")
#         # echo "stat_output: $stat_output"
#         # Extract the number of insertions
#         insertions=$(echo "$stat_output" | grep -o '[0-9]* insertion' | awk '{print $1}')

#         # Extract the number of deletions
#         deletions=$(echo "$stat_output" | grep -o '[0-9]* deletion' | awk '{print $1}')

#         # Handle cases where no insertions or deletions were found
#         insertions=${insertions:-0}
#         deletions=${deletions:-0}

#         # Append to CSV file
#         echo "$class_name,$changes,$total,$insertions,$deletions" >> "$csv_file"
        
#         # echo "$file changed $changes times in $total commits"
#     fi
# done


#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <project_name> <project_path> <output-path> <git_hash>"
    exit 1
fi

# Start time tracking
# start_time=$(date +%s)

project_name=$1
original_dir=$(pwd)
project_path=$2
output_path=$3
git_hash=$4
csv_file="$original_dir/changes_with_line_fixed_3/$project_name/$output_path"

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

# checkout to hash
git checkout $git_hash

# Get the list of files changed between the two commits
changed_files=$(git log --name-only -l0 --pretty=format: $start_hash..HEAD | grep -v '^$' | sort | uniq)

# if the directory does not exist, create it
if [ ! -d "$original_dir/changes_with_line_fixed_3/$project_name" ]; then
    mkdir -p "$original_dir/changes_with_line_fixed_3/$project_name"
fi

# Create the CSV file
echo "ClassName,Changes,TotalCommits,Insertions,Deletions" >> "$csv_file"
if [ $? -ne 0 ]; then
    echo "Error: Unable to create CSV file at $csv_file"
    exit 1
fi
echo "CSV file created at: $csv_file"
# 
# Function to calculate insertions and deletions using git log --numstat
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
        class_name=$(basename "$file" .java)
        creation_hash=$(git log --find-renames --diff-filter=A -- "$file" | head -n 1 | cut -d ' ' -f 2)
        changes=$(git rev-list --count $start_hash..HEAD -- "$file")
        total=$(git rev-list --count $creation_hash..HEAD)
        
        # Calculate insertions and deletions
        ins_del=$(calculate_insertions_deletions "$file" "$creation_hash" "HEAD")
        insertions=$(echo $ins_del | cut -d' ' -f1)
        deletions=$(echo $ins_del | cut -d' ' -f2)
        
        # Append to CSV file
        echo "$class_name,$changes,$total,$insertions,$deletions" >> "$csv_file"
    fi
done

# End time tracking
# end_time=$(date +%s)

# # Calculate the time difference
# execution_time=$((end_time - start_time))

echo "Analysis complete. Results saved to $csv_file"