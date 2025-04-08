# Score Uploader Elearn

Usage:
main.py - Upload the grade in score.csv and pdf files in uploads/ folder to elearn, the student_id in pdf name has to be the same as the one in score.csv
- {prefix}{student_id}.pdf in uploads/ -> {student_id}, {student_grade} in score.csb
modify both course_id and homework_id to upload it to the correct homework and class platform, change hw prefix depending on the regulations, default prefix HW6_ 
- HW6_{student_id} then change prefix to uploads/HW6_

move_to_root.py - Utility script to separate each pdf in each student folder into the root folder (since the default in elearn is to upload it to folder first)
- python move_to_root.py {root_folder}

Possible bug : 
Since some of them are hardcoded, if the program is terminated because of slow internet, so it couldn't submit in time, the pdf that has been submitted has to be deleted and 
in the score.csv, the student's grade that has been submitted also has to be deleted
if not deleted, it will resubmit and reupload 2 pdfs
