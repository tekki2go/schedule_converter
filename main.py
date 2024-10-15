# Copyright (C) 2024  Marc Heß (tekki2go)

import requests
import os

# Settings
download_url = 'https://owncloud.dhbw-heidenheim.de/index.php/s/ddgLVIobcYSZi0e/download'
download_dir = 'schedule_download/'
temp_dir = 'temp/'
output_dir = 'output/'

# Download file path
file_path = os.path.join(download_dir, "Semester-Planung.zip")

# DEBUGGING
enable_downloads = False

#region Setup
# Create directories
for directory in [download_dir, temp_dir, output_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

#endregion

#region 1. download ZIP

##### DOWNLOAD ZIP #####

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
#endregion

#region 2. extracting ZIP

##### EXTRACT ZIP #####

import shutil

try:    
    # Extract Zip file
    shutil.unpack_archive(file_path, download_dir)
    print(f"Zip file extracted successfully to {download_dir}")
except Exception as e:
    print(f'Could not extract zip file! \n{e}')

#endregion

#region 3. get newest PDF

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

#region 4. extract page content from PDF

##### EXTRACT PAGE CONTENT FROM PDF #####

# Using pdfplumber to make data extraction more accurate
import pdfplumber

extracted_text = []
with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        extracted_text.append(pdf.pages[page_num].extract_text())
print("extracted text from pdf.")
#endregion

#region 5. Save CSV files
import pandas as pd

with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        # Extract text for the current page
        extracted_text = pdf.pages[page_num].extract_text()
        
        # Split the text into lines
        lines = extracted_text.split('\n')
        
        # Process the lines to extract table-like data
        data = []
        for line in lines:
            row = line.split()  # Split by spaces
            data.append(row)
        
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data)
        
        # Save each page's DataFrame as a separate CSV file
        csv_path = f'{temp_dir}/converted_page_{page_num + 1}.csv'
        df.to_csv(csv_path, index=False)

        print(f"CSV for page {page_num + 1} saved at: {csv_path}")



#region LICENSE
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
#endregion