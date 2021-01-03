"""
List the name and file path of each feature class in a geodatabase
Author: Cara Whalen
"""

import arcpy 
from arcpy import env 
import os 

# Define the workspace
env.workspace = r"L:\admin\special_projects\CODEX\CPW_Data_for_CODEX_20201222\Statewide_Data_Public.gdb"

# List the feature datasets in the geodatabase
datasetList = arcpy.ListDatasets("*", "Feature")  
datasetList.sort()

# Loop through the feature datasets
for dataset in datasetList:
    # List each feature class in the feature dataset
    fcList = arcpy.ListFeatureClasses("*","",dataset)
    fcList.sort()
    # Loop through the feature classes
    # Print the feature class name and file path
    for fc in fcList:
        desc = arcpy.Describe(fc)
        print (fc + "," + desc.path+ "\\" +dataset+"\\"+fc) 
