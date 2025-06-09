import os
import shutil
import sys

def main(working_dir):
    if not os.path.isdir(working_dir):
        print(f"Error: {working_dir} is not a valid directory.")
        return

    # Define target folders
    pdf_dir = os.path.join(working_dir, 'reports')
    s_dir = os.path.join(working_dir, 'code')

    # Create target folders if not exist
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(s_dir, exist_ok=True)

    # 1. First handle files directly in the working directory
    for file in os.listdir(working_dir):
        src_file = os.path.join(working_dir, file)
        if os.path.isfile(src_file):
            if file.lower().endswith('.pdf'):
                shutil.move(src_file, os.path.join(pdf_dir, file))
                print(f"Moved PDF: {file}")
            elif file.endswith('.S'):
                shutil.move(src_file, os.path.join(s_dir, file))
                print(f"Moved .S: {file}")

    # 2. Then handle subdirectories (excluding the target folders)
    for item in os.listdir(working_dir):
        path = os.path.join(working_dir, item)
        if os.path.isdir(path) and path not in [pdf_dir, s_dir]:
            pdf_found = False
            s_found = False

            for file in os.listdir(path):
                src_file = os.path.join(path, file)
                if os.path.isfile(src_file):
                    if file.lower().endswith('.pdf'):
                        shutil.move(src_file, os.path.join(pdf_dir, file))
                        pdf_found = True
                        print(f"Moved PDF: {file} from {item}")
                    elif file.endswith('.S') or file.endswith('.s'):
                        shutil.move(src_file, os.path.join(s_dir, file))
                        s_found = True
                        print(f"Moved .S/.s: {file} from {item}")

            # Delete only if files were moved and folder is now empty
            if (pdf_found or s_found):
                try:
                    os.rmdir(path)
                    print(f"Deleted folder: {path}")
                except OSError:
                    print(f"Skipped deletion (not empty): {path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python code_pdf_separator.py /path/to/working_dir")
    else:
        main(sys.argv[1])