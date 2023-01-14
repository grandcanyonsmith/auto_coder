### Ideas for new features

# 1. New work flow - Every time that a file is edited, instead of changing the original file, it will copy the from the original file, but create a temp file with the same name but add _tmp to it. After the code on the tmp file is created, it will have an 'evaluate_changes_between_old_and_new_files' function that will get the 'git diff' between the two files, but that into a string, and then ask OPENAIs' gpt-3, "What changes have been made between these two files?". Then it will save that summary of the changes to "files/text/changes_made.txt file". After that it will try to run the new code. If successful, then it will replace the old file content with the new and erase the temp file

# 2. First step in creating something is create a scaffold. "What are all of the files needed to make this?" Then execute the creation of the folders.

# 3. Iterate over every file in a folder for improvement

# 4. Data store the MAIN goal and sub-goals then append them in front of commands
