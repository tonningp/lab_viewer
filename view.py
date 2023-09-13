#!/usr/bin/env python3

import zipfile
import re
import os
import sys
import subprocess

def extract_filename(filename):
    # Using regex to extract the email from the filename
    #email_regex = r'[\w\.-]+@[\w\.-]+'
    #match = re.search(email_regex, filename)
    #if match:
    #    return match.group()
    #return None
    return os.path.splitext(filename)[0]

def check_comment(input_string):
    import re

    # Sample input string
    # input_string = """
    # /*
    #     File: main.cpp
    #     Description: This is a sample code file.
    #     Author: John Doe
    #     Email: johndoe@example.com
    #     Course#: CS101
    #     Section#: A
    #     Date: 2023-09-12
    # */ 
    # """

    # Define a regular expression pattern to match the desired pattern
    pattern = r"/\*\s+File:\s+(?P<file_name>.*?)\s+Description:\s+(?P<description>.*?)\s+Author:\s+(?P<author>.*?)\s+Email:\s+(?P<email>.*?)\s+Course#:\s+(?P<course>.*?)\s+Section#:\s+(?P<section>.*?)\s+Date:\s+(?P<date>.*?)\s+\*/"

    # Use re.search to find the pattern in the input string
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        # Extract information from the match using group names
        file_name = match.group('file_name')
        description = match.group('description')
        author = match.group('author')
        email = match.group('email')
        course = match.group('course')
        section = match.group('section')
        date = match.group('date')

        # Print the extracted information
        print("File:", file_name.strip())
        print("Description:", description.strip())
        print("Author:", author.strip())
        print("Email:", email.strip())
        print("Course#:", course.strip())
        print("Section#:", section.strip())
        print("Date:", date.strip())
    else:
        print("Pattern not found in the input string.")
    
def main():
    # Path to the main zip file containing other zip files
    if len(sys.argv) <= 1:
        print(f"Usage: python {sys.argv[0]} <zipfile>")
        sys.exit(1)

    main_zip_path = sys.argv[1]

    # Create a temporary directory to extract zip files
    temp_dir = 'temp_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    
    # Open the main zip file
    with zipfile.ZipFile(main_zip_path, 'r') as main_zip:
        for fileinfo in main_zip.infolist():
            email = extract_filename(fileinfo.filename)
            print(fileinfo.filename)
            if email:
                # Create a new name for the zip file based on the email
                new_zip_name = f"{email}.zip"

                # Extract and rename the zip file
                main_zip.extract(fileinfo, temp_dir)
                os.rename(os.path.join(temp_dir, fileinfo.filename), os.path.join(temp_dir, new_zip_name))

                # Unzip the renamed zip file
                with zipfile.ZipFile(os.path.join(temp_dir, new_zip_name), 'r') as sub_zip:
                    sub_zip.extractall(temp_dir)

                    # Rename 'main.cpp' to 'main_<email>.cpp'
                    os.rename(
                        os.path.join(temp_dir, 'main.cpp'),
                        os.path.join(temp_dir, f'main_{email}.cpp')
                    )
                    with open(f'main_{email}.cpp','w') as mainfile:
                        
                    # Open the renamed 'main.cpp' file in Vim
                    subprocess.run(['vim', os.path.join(temp_dir, f'main_{email}.cpp')])

if __name__ == '__main__':
    main()
