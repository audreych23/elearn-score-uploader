import os
import shutil
import sys

if len(sys.argv) < 2:
    print("Usage: python test.py <folder_path>")
    sys.exit(1)

root_dir = sys.argv[1]

if not os.path.isdir(root_dir):
    print(f"Error: '{root_dir}' is not a valid directory.")
    sys.exit(1)

# Collect folder and file info
subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

print(f"Found {len(subdirs)} subfolders in '{root_dir}':")
for subdir in subdirs:
    print(f"- {subdir}")

confirm = input("Move all files to root and delete folders? (y/n): ").lower()
if confirm != 'y':
    print("Aborted.")
    sys.exit(0)
    
# loop through all subdirectories 
for subdir in subdirs:
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        for file_name in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file_name)
            if os.path.isfile(file_path):
                # move file to aaa/
                shutil.move(file_path, os.path.join(root_dir, file_name))
        # delete the now-empty folder
        os.rmdir(subdir_path)
