# Score Uploader Elearn

Possible bug : 
Since some of them are hardcoded, if the program is terminated because of slow internet, so it couldn't submit in time, the pdf that has been submitted has to be deleted and 
in the score.csv, the student's grade that has been submitted also has to be deleted
if not deleted, it will resubmit and reupload 2 pdfs

Seems like it does weird thing sometimes?

mv.py doesn't work yet (it is an utility function to use to separate each pdf in each student folder into one folder such as uploads)
Without this, the user has to manually move the .pdf files from the student folder to the uploads folder.