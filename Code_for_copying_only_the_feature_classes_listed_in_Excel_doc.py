# Code used to automate the process of copying specific feature classes from SAM or NonSAM to a file geodatabase
# Only the feature classes listed in the excel document are copied to the file geodatabase
# Domains are copied over, but relationship classes and related tables are NOT copied
# Code written by Cara Whalen 12/22/2020

import arcpy
import pandas as pd
import os

# Import the excel file containing the CODEX feature class list
df = pd.read_excel(r'L:\parks\temp\Cara\CODEX_data\CODEX_Feature_Class_List.xlsx', sheetname='NonSAM_Public')
CODEXlist = df['CODEX_Feature_Class'].tolist()
print("Imported list of CODEX feature classes.")

# Define the workspace
arcpy.env.workspace = r"Database Connections\NonSAM.sde"
print("Defined the workspace.")

# Define the input geodatabase
inputGDB = r"Database Connections\NonSAM.sde"
print("Defined the input geodatabase.")

# Define the output geodatabase
outputGDB = r"L:\admin\special_projects\CODEX\CPW_Data_for_CODEX_20201222\Statewide_Data_Public.gdb"
print("Defined the output geodatabase.")

# Define the spatial reference as NAD83 UTM Zone 13N
sr = arcpy.SpatialReference(26913)
print("Defined the spatial reference.")

# List the feature classes in the workspace
# Check whether each feature class is in the CODEX list
# If the feature class is in the CODEX list, copy it to the output GDB
datasetList = arcpy.ListDatasets("*", "Feature")
datasetList.sort()
print("Listed the feature datasets in the workspace.")
for dataset in datasetList:  
    datasetName = dataset.split('.')[-1:][0]
    print("Created name variable for "+dataset+" feature dataset")
    fcList = arcpy.ListFeatureClasses("*","",dataset)
    fcList.sort()
    print("Listed feature classes in "+dataset+" feature dataset.")
    print("---")  
    for fc in fcList:
        print("Checking if the "+fc+" feature class is in the CODEX list.")
        if fc in CODEXlist:
            print(fc+" is in the CODEX list!")
            fcName = fc.split('.')[-1:][0]
            print("Created name variable for the "+fc+" feature class.")
            if arcpy.Exists(os.path.join(outputGDB,datasetName)):
                try:
                    arcpy.CopyFeatures_management(os.path.join(inputGDB,dataset,fc),os.path.join(outputGDB,datasetName,fcName))
                    print("Copied "+fcName+" feature class.")
                    print("---")
                except arcpy.ExecuteError:
                    print("Something went wrong when copying the "+fc+" feature class.")
                    print(arcpy.GetMessages())
            else:
                arcpy.CreateFeatureDataset_management(outputGDB,datasetName,sr)
                print("Created "+datasetName+" feature dataset.")
                try:
                    arcpy.CopyFeatures_management(os.path.join(inputGDB,dataset,fc),os.path.join(outputGDB,datasetName,fcName))
                    print("Copied "+fcName+" feature class.")
                    print("---")
                except arcpy.ExecuteError:
                    print("Something went wrong when copying the "+fc+" feature class.")
                    print(arcpy.GetMessages())
        else:
            print(fc+" was not found in the CODEX list.")
            print("---")

print("All done!")
