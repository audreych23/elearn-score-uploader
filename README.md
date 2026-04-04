# Score Uploader Elearn
This script automates the process of submitting scores and uploading PDF files to NTHU's eLearn platform using Selenium.

## Features
- Inputs the grades from a CSV file
- Optionally uploads PDF submissions per student based on their student ID
- Supports score-only mode with `--no-pdf` flag (no PDF upload needed)
- Supports gradebook mode with `--gradebook_id` for quizzes and other non-assignment grade items

**For example, if uploading PDFs and a CSV row contains `109006273,100`, the script expects to find a PDF named like `<prefix>109006273.pdf`.**

## Requirements

- Python 3.6+
- Google Chrome browser
- ChromeDriver (version must match your Chrome version)
- Python packages:
  - selenium

Install required Python packages:

```bash
pip install selenium
```

## Usage
```bash
python main.py --help
```

### Score + PDF upload
```bash
python main.py --prefix "HW5_" --dir uploads --score score.csv --course_id "{your_course_id}" --homework_id "{your_homework_id}"
```

### Score only (no PDF)
```bash
python main.py --no-pdf --score score.csv --course_id "{your_course_id}" --homework_id "{your_homework_id}"
```

### Gradebook mode (quizzes, non-assignment items)
For grade items that use the gradebook singleview page (e.g., quizzes), use `--gradebook_id` instead of `--homework_id`. The gradebook ID is the `itemid` parameter in the URL:
`https://elearn.nthu.edu.tw/grade/report/singleview/index.php?id={course_id}&item=grade&itemid={gradebook_id}`

```bash
python main.py --score score.csv --course_id "{your_course_id}" --gradebook_id "{your_gradebook_id}"
```

| Argument        | Required | Description                                             | Default       |
|-----------------|----------|---------------------------------------------------------|---------------|
| `--prefix`      | N*       | Prefix of the PDF filenames (e.g., `HW5_`)              | None          |
| `--dir`         | N*       | Directory where PDFs are stored                         | `uploads`     |
| `--score`       | N        | CSV file path containing student IDs and their scores   | `score.csv`   |
| `--course_id`   | Y        | Course ID from the eLearn URL                           | None          |
| `--homework_id`  | N**      | Homework ID from the eLearn assignment grading page URL | None          |
| `--gradebook_id` | N**      | Grade item ID for gradebook mode (quizzes, etc.)        | None          |
| `--no-pdf`      | N        | Only upload scores, skip PDF upload                     | `false`       |

*`--prefix` and `--dir` are required when uploading PDFs (i.e., when `--no-pdf` is **not** used).

**Either `--homework_id` or `--gradebook_id` must be provided. If `--gradebook_id` is provided, gradebook mode is used and `--homework_id` is ignored.

## PDF Filename Format

Each PDF file in the `--dir` directory must follow this naming format:

```
<prefix><student_id>.pdf
```

For example, if your prefix is `HW5_` and a student ID is `109006273`, the file must be named:

```
HW5_109006273.pdf
```

Ensure all PDF files strictly follow this pattern for the script to correctly locate and upload them.

## CSV Format
The CSV file should follow this format:

```csv
109006273,90
113065428,85
```
No headers. Each line is:

```csv
<student_id>,<score>
```

## Known Issue:

If the program is interrupted (e.g., due to slow internet or timeout), a partially submitted grade or uploaded PDF may remain in the system.
 
When the script is rerun:
- The script will re-upload the PDF, resulting in multiple files for the same student.
- The score will be submitted again, possibly overwriting or duplicating the grading process.

## Temporary Workaround
After an interruption:
- Manually delete any already uploaded PDFs on the elearn platform before rerunning the script.
- Then, remove the corresponding student entry from score.csv to prevent duplicate submissions.

## Utilities File
### move_to_root.py
This utility script helps you reorganize PDF submissions by moving each PDF from individual student folders into a single root folder.

This is useful because eLearn typically stores each uploaded submission inside its own folder.

#### Usage
```
python move_to_root.py {root_folder}
```
- {root_folder} is the path to the directory containing all student submission folders.
- The script will move all PDF files from subdirectories into this root folder.

