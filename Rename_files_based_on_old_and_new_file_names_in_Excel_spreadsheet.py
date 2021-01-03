"""
This script can be used to rename files in a directory
The script reads an Excel document that has the old file names in one column and the new file names in another column
The script compares each file in the directory to the old file list
If a file is in the old file list, it is renamed to the corresponding name from the new file list
Created 12/27/2020
Author: Cara Whalen
"""

import os
import pandas as pd

# Read Excel file
excelDoc = pd.read_excel('D:\data_organization_files\SLBE_BenthicVideo_ALLcompiled_12262020.xlsx', sheetname="Combine") 

# Create a list of the old file names from the Excel doc
oldFileNameList = excelDoc['Old_File_Name'].tolist()

# Create a list of the new file names from the Excel doc
newFileNameList = excelDoc['New_File_Name_w_Etx'].tolist()

# Define the directory containin the video files that need to be renamed
directory = r'D:\SLBE_Videos_Organized_Renamed'

# Loop through the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        # Compare each file in the directory to the old file list
        # If the file is in the new file list, rename the file with the corresponding name in the new file list
        if file in oldFileNameList:
            fileIndex = oldFileNameList.index(file)
            oldName = oldFileNameList[fileIndex]
            oldPath = os.path.join(root, oldName)
            newName = newFileNameList[fileIndex]
            newPath = os.path.join(root, newName)
            os.rename(oldPath, newPath)
            print("Changed "+oldPath+" to "+newPath)

print("All done!")
