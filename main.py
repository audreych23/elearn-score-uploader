from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os, time


# using chrome 
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

## Setting
# Please set this to the correct course id and homework id
# https://elearn.nthu.edu.tw/enrol/index.php?id=???
course_id = '35343'
# https://elearn.nthu.edu.tw/mod/assign/view.php?id=154385&action=grading
homework_id = '190234'
# modify this depending on the structure of the naming rule of the hw
homework_prefix = "uploads/HW6_"

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


def upload_score_pdf(student_id, score):
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
    grade_button.send_keys(score)

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

# uncomment this later for actual running (the for loop)
data = loadCSV("score.csv")
# print(data)
manual_login()
move_course()
# test 
# upload_score_pdf('107065804', '100')
# print(data)
for student_id, score in data:
    score = "100" if float(score) >= 100 else score
    upload_score_pdf(student_id, score)


#bug : if no submission then it broke ;), if no submission then maybe just input mnaully