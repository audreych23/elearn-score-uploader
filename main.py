from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os, time, re
import sys

import argparse



# Wait for login
def manual_login():
    driver.get("https://elearn.nthu.edu.tw/")
    print("Waiting until succesful login......")
    wait = WebDriverWait(driver, 120)
    wait.until(lambda d : d.current_url == "https://elearn.nthu.edu.tw/my/" or d.current_url == "https://elearn.nthu.edu.tw/my/index.php?lang=zh_tw")
    print("login ok")

def move_course():
    driver.get('https://elearn.nthu.edu.tw/enrol/index.php?id=' + course_id)
    print('Succesfully entered the course')

def loadCSV(filepath):
    res = []
    with open(filepath) as f:
        while True:
            buf = f.readline()
            if not buf:
                break
            v = buf.strip().split(',')
            res.append(v)
    return res


def upload_score_gradebook(data):
    """Upload scores via the gradebook singleview page (for quizzes, etc. with no PDF)."""
    driver.get(f"https://elearn.nthu.edu.tw/grade/report/singleview/index.php?id={course_id}&item=grade&itemid={gradebook_id}&lang=en&edit=on")
    time.sleep(3)

    # Build a lookup dict from CSV: student_id -> score
    score_map = {sid: sc for sid, sc in data}

    # Find all rows in the grade table
    rows = driver.find_elements(By.CSS_SELECTOR, "table.generaltable tbody tr")

    filled = 0
    for row in rows:
        try:
            user_cell = row.find_element(By.CSS_SELECTOR, "th.cell.c0")
        except NoSuchElementException:
            continue

        # The <a> contains a <span class="userinitials"> (e.g. "IN") followed by
        # a text node like "111006226 江南棠 NAJMA PREVIA JATI".
        # .text includes both, so we extract the student ID via regex.
        cell_text = user_cell.text.strip()
        if not cell_text:
            continue

        id_match = re.search(r'(Z[PC]-\w+|\d{5,})', cell_text)
        if not id_match:
            print(f"Skipping row — no student ID found in: {cell_text}")
            continue
        student_id = id_match.group(1)

        if student_id not in score_map:
            print(f"Skipping {student_id} — not in CSV")
            continue

        score = score_map[student_id]
        score = "100" if float(score) >= 100 else score

        # Find the grade input in the grade cell (c2)
        try:
            grade_cell = row.find_element(By.CSS_SELECTOR, "td.cell.c2")
            grade_input = grade_cell.find_element(By.CSS_SELECTOR, "input[type='text']")
            grade_input.clear()
            grade_input.send_keys(score)
            filled += 1
            print(f"Filled: {student_id} -> {score}")
        except NoSuchElementException:
            print(f"Could not find grade input for {student_id}")
            continue

    print(f"Filled {filled} grades. Please review and save manually, or press Enter to auto-save.")

    # Try to find and click the save button
    try:
        save_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        input("Press Enter to save grades (or Ctrl+C to cancel)...")
        save_button.click()
        print("Grades saved!")
    except NoSuchElementException:
        print("Could not find save button — please save manually in the browser.")


def upload_score_pdf(student_id, score, skip_pdf=False):
    driver.get("https://elearn.nthu.edu.tw/mod/assign/view.php?id="+ homework_id + "&action=grader" + "&lang=en")

    search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-region='user-selector']//div[@class='alignment']//span//input")))

    try:
        search_button.send_keys(student_id)
    except:
        print(f"can't find student id...maybe student isn't enrolled in the course")
        with open("output.txt", "a") as f:
            f.write(student_id)
    # increase time delay if it does not change
    time.sleep(3)
    search_button.send_keys(Keys.RETURN)
    # search_button.submit()
    time.sleep(5)

    # score submission
    grade_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_grade"]')))
    grade_button.clear()
    grade_button.send_keys(score)

    if skip_pdf:
        # save changes (score only, no PDF)
        button = driver.find_element(By.XPATH, "//button[@type='submit' and @name='savechanges']")
        button.click()
        print(f'success (score only): {student_id}')
        return

    # for exchange student they will start with ZP-X______ something in the system however, submission normally starts with X
    # for student outside of this school, they will start with ZC-______ in the system however, submission normally starts wth the student id
    if student_id[0] == 'Z':
        student_id = student_id[3:]

    file_path_rel = homework_prefix + student_id + ".pdf"
    filepath =  os.path.abspath(file_path_rel)


    if not os.path.exists(filepath):
        print(f"No submission for student with student id : {student_id}")
        time.sleep(2)

        # save changes
        button = driver.find_element(By.XPATH, "//button[@type='submit' and @name='savechanges']")
        button.click()

        # confirmation_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='confirmation-buttons text-xs-right']//input[@type='button']")))
        # confirmation_button.click()
        # time.sleep(1)
        print(f'success: {student_id}')
        return

    # pdf
    upload_button = driver.find_element(By.XPATH, "//a[@role='button' and @title='Add...']")
    upload_button.click()
    time.sleep(2)

    upload_tab = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@role="tab" and .//span[contains(text(), "Upload a file")]]')))
    upload_tab.click()

    # drop pdf
    drop_area = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,  '//input[@type="file" and @name="repo_upload_file"]')))

    print(filepath)

    drop_area.send_keys(filepath)

    # upload pdf
    upload_file_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")))
    upload_file_button.click()

    # wait until pdf finish uploading
    time.sleep(7)

    # save changes
    button = driver.find_element(By.XPATH, "//button[@type='submit' and @name='savechanges']")
    button.click()

    # confirmation_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='confirmation-buttons text-xs-right']//input[@type='button']")))
    # confirmation_button.click()
    # time.sleep(1)
    print(f'success: {student_id}')

if __name__ == '__main__':
    # ---------------------- ARGUMENT PARSING ----------------------
    parser = argparse.ArgumentParser(description="Upload scores and PDFs to NTHU eLearn")
    parser.add_argument("--prefix", default="", help="Homework file prefix, e.g. 'HW5_'")
    parser.add_argument("--dir", default="uploads", help="Directory containing PDF files")
    parser.add_argument("--score", required=True, default="score.csv", help="Path to CSV file containing scores")
    parser.add_argument("--course_id", required=True, default="", help="Course ID from URL")
    parser.add_argument("--homework_id", default="", help="Homework ID from URL (for assignment grader)")
    parser.add_argument("--gradebook_id", default="", help="Grade item ID for gradebook mode (see README for details)")
    parser.add_argument("--no-pdf", action="store_true", help="Only upload scores, skip PDF upload")

    args = parser.parse_args()

    no_pdf = args.no_pdf
    gradebook_mode = bool(args.gradebook_id)

    if gradebook_mode:
        # Gradebook mode: only need course_id, gradebook_id, and score CSV
        pass
    elif not no_pdf and (not args.prefix or not args.dir):
        sys.exit("Error: --prefix and --dir are required when uploading PDFs. Use --no-pdf to skip PDF upload.")

    if not gradebook_mode and not args.homework_id:
        sys.exit("Error: either --homework_id or --gradebook_id is required.")

    homework_prefix = os.path.join(args.dir, args.prefix) if not no_pdf and not gradebook_mode else ""
    course_id = args.course_id
    homework_id = args.homework_id
    gradebook_id = args.gradebook_id
    score_csv_path = args.score

    # using chrome
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # Validate course_id
    if args.course_id.strip() == "":
        sys.exit("Error: --course_id cannot be an empty string.")

    ## Setting
    # Please set this to the correct course id and homework id
    # https://elearn.nthu.edu.tw/enrol/index.php?id=???
    # course_id = '35343'
    # https://elearn.nthu.edu.tw/mod/assign/view.php?id=154385&action=grading
    # homework_id = '192279'
    # modify this depending on the structure of the naming rule of the hw
    # homework_prefix = "uploads/HW2_"

    print("course_id:", course_id)
    print("score_csv:", score_csv_path)
    if gradebook_mode:
        print("gradebook_id:", gradebook_id)
    else:
        print("homework_id:", homework_id)
        print("hw_prefix:", homework_prefix)

    data = loadCSV(score_csv_path)
    manual_login()
    move_course()

    if gradebook_mode:
        upload_score_gradebook(data)
    else:
        for student_id, score in data:
            score = "100" if float(score) >= 100 else score
            upload_score_pdf(student_id, score, skip_pdf=no_pdf)


#bug : if no submission then it broke ;), if no submission then maybe just input mnaully