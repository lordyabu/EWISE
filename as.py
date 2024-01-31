import os

# Define the paths to the two directories
dir1_path = "data"
dir2_path = "data_old"

# Get a list of file names in the first directory
dir1_files = os.listdir(dir1_path)

# Get a list of file names in the second directory
dir2_files = os.listdir(dir2_path)

# Find files that are in dir1 but not in dir2
files_only_in_dir1 = [file for file in dir1_files if file not in dir2_files]

# Print the list of files only in dir1
print("Files only in dir1:", files_only_in_dir1)
