"""
This script can be used to list all of the files in a directory
The output is a csv file containing the file names, file pathes, and file types
As it's written, the script only lists video files (.mp4, .mpg, .avi, and .MP4)
Created 11/1/2020
Author: Cara Whalen
"""
import os
import csv

#define the directory
directory =r'F:\SLBE\SLBE_08_Videos_FieldData_cara'

#create list to store all the file names
fileList = []

#list everything in the directory
for root, dirs, files in os.walk(directory):
	for file in files:
        #append the file path and name to the list
		fileList.append([os.path.join(root,file),file])

#add file extensions to the list
for fileSubList in fileList:
    try:
        fileName = fileSubList[1]
        #get the file extension
        name, extension = os.path.splitext(fileName)
        #append the file extension to the list
        fileSubList.append(extension)
    except:
        pass

# name of csv file  
filename = r"F:\data_organization_files\video_list_20210102_final_check.csv"
headers = ["File Path","File Name","File Extension"]
    
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
    # writing the headers  
    csvwriter.writerow(headers) 
    for fileSubList in fileList:
        if fileSubList[2] == ".mp4" or fileSubList[2] == ".mpg" or fileSubList[2] == ".avi" or fileSubList[2] == ".MP4":
            csvwriter.writerow(fileSubList) 


            
           
