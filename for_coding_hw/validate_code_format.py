import os
import sys
import json
import re
import shutil

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def validate_filename(filename, hw_name, task_names):
    if not filename.endswith('.S'):
        return False

    base = filename[:-2]
    parts = base.split('_')

    if len(parts) < 3:
        return False

    hw = parts[0]
    task = '_'.join(parts[1:-1])
    student_id = parts[-1]

    if hw != hw_name:
        return False

    if task not in task_names:
        return False

    if not re.fullmatch(r'\d{9}', student_id):
        return False

    return True

def main(folder_path, config_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    try:
        config = load_config(config_path)
        hw_name = config['hw_name']
        task_names = config['task_names']
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    wrong_dir = os.path.join(folder_path, 'wrong_submission')
    os.makedirs(wrong_dir, exist_ok=True)

    print(f"Checking .S files in: {folder_path}")
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path):
            if validate_filename(fname, hw_name, task_names):
                print(f"VALID: {fname}")
            else:
                print(f"INVALID: {fname}")
                shutil.move(full_path, os.path.join(wrong_dir, fname))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python validate_s_files.py <folder_path> <config.json>")
    else:
        main(sys.argv[1], sys.argv[2])