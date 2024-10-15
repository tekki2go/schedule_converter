import requests
import os

# Setting
download_url = 'https://owncloud.dhbw-heidenheim.de/index.php/s/ddgLVIobcYSZi0e/download'
download_dir = 'schedule_download/'

# Download file path
file_path = os.path.join(download_dir, "Semester-Planung.zip")

# DEBUGGING
enable_downloads = False

if enable_downloads:
    try:
        # Download the file
        response = requests.get(download_url)

        # Save the file in the download directory
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f'File downloaded successfully to {file_path}')
    except Exception as e:
        print(f'File download failed! \n{e}')
else:
    print(f'Skipped download...')

#region 1. extracting ZIP

##### EXTRACT ZIP #####

import shutil

try:    
    # Extract Zip file
    shutil.unpack_archive(file_path, download_dir)
    print(f"Zip file extracted successfully to {download_dir}")
except Exception as e:
    print(f'Could not extract zip file! \n{e}')

#endregion

#region 2. get newest PDF

##### GET NEWEST PDF #####

# File path of extracted files
file_path = os.path.join(download_dir, "Semester-Planung/")

files = [f for f in os.listdir(file_path) if f.startswith("VP_")]

# Get the newest pdf based on modification time
if os.listdir():
    newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(file_path, f)))
else:
    newest_file = None

pdf_path = os.path.join(file_path, newest_file)

print(f'Newest PDF file: {pdf_path}')
#endregion

#region 3. extract page content from PDF

##### EXTRACT PAGE CONTENT FROM PDF

# Using pdfplumber to make data extraction more accurate
import pdfplumber

extracted_text = []
with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        extracted_text.append(pdf.pages[page_num].extract_text())

extracted_text[:1]
#endregion

