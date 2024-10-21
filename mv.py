import sys
import shutil
import os
import glob

# usage : moves all files inside a bunch of folder outsides into another folder
if __name__ == "__main__":
    # Check the number of command-line arguments (including the script name)
    argc = len(sys.argv)

    if argc != 3:
        print("Usage: python mv.py <source_folder_that_contains_all_folders> <dest_folder> ...")
        print("Please provide two args.")
        exit()

    # Access command-line arguments (argv)
    source = sys.argv[1]  # First argument after the script name
    dest = sys.argv[2]  # Second argument after the script name

    # Create the directory
    print(os.listdir(source))
    print(os.path.join(source, "/*/*.pdf"))
    files = glob.glob(source + "/*/*.pdf") 
    print(files)

    # for f in files:
    #     if os.path.isfile(f):
    #         shutil.move(f, dest)



