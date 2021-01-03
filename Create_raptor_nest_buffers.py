"""
Creates buffers around raptor nests
Buffer size (meters) is based on species
Input is a point feature class of the raptor nests
Output is a poly feature class of the nest buffers
Only buffers the raptor nests that have been active in the past five years
Prints message containing the nests it was not able to buffer (likely due to a problem with the species)
Cara Whalen 12/31/2020
"""

import arcpy

# Define the raptor nest feature class to be buffered
raptNests = r"L:\admin\special_projects\CODEX\CPW_Data_for_CODEX_20201222\Statewide_Data_Private.gdb\Raptor\CPWRaptorNests"

# Define the the past five years
startYear = "2016"
startYearFormatted = "date \'"+startYear+"-01-01 00:00:00\'"
SQLexpression = 'LASTSURVEYDATE >='+ startYearFormatted

# Define the temporary feature class
tempFC = r"L:\parks\public\colorado\biology\animals\Temp_Folder\Temp.gdb\cpw_raptor_nests_past_5years"

# If there is as an old version of the temp feature class, delete it
if arcpy.Exists(tempFC):
    arcpy.Delete_management(tempFC)
    print("Deleted the old temp feature class")

# Define the output feature class
outputFC = r"L:\admin\special_projects\CODEX\CPW_Data_for_CODEX_20201222\Statewide_Data_Private.gdb\Raptor\CPWRaptorNestsBuffered"

# If there is as an old version of the nest buffers feature class, delete it
if arcpy.Exists(outputFC):
    arcpy.Delete_management(outputFC)
    print("Deleted the old nest_buffers feature class")

# Select the nests that have been active in the past five years and 
# create a new temporary feature class
arcpy.Select_analysis(raptNests, tempFC, SQLexpression)
print("Selected the nests that have been active within the past five years")
print("Created a temporary feature class containing the selection")

# Add a field for the buffer distance
arcpy.AddField_management(tempFC, "Buff_Dist", "SHORT", "", "", "", "", "NULLABLE")
print("Added a field for the buffer distance")

# Define function for calculating buffer distances
codeblock = """
def buffDist(species):
    if species == "Accipiter Spp":
        return 0
    if species == "American Kestrel":
        return 50
    if species == "Bald Eagle":
        return 800
    if species == "Barn Owl":
        return 200
    if species == "Burrowing Owl":
        return 50
    if species == "Buteo Spp":
        return 0
    if species == "Common Raven":
        return 0
    if species == "Cooper's Hawk":
        return 200
    if species == "Eastern Screech-Owl":
        return 200
    if species == "Ferruginous Hawk":
        return 800
    if species == "Golden Eagle":
        return 800
    if species == "Great Horned Owl":
        return 100
    if species == "Long-eared Owl":
        return 200
    if species == "Northern Goshawk":
        return 800
    if species == "Northern Harrier":
        return 400
    if species == "Northern Pygmy-Owl":
        return 400
    if species == "Osprey":
        return 400
    if species == "Peregrine Falcon":
        return 800
    if species == "Prairie Falcon":
        return 800
    if species == "Red-tailed Hawk":
        return 600
    if species == "Scrape Large":
        return 0
    if species == "Sharp-shinned Hawk":
        return 200
    if species == "Stick Nest Large":
        return 0
    if species == "Stick Nest Small":
        return 0
    if species == "Swainson's Hawk":
        return 400
    if species == "Turkey Vulture":
        return 800
    if species == "Unknown":
        return 0
    if species == "Western Screech-Owl":
        return 200
    else:
        return 0"""

# Caculate field to determine the buffer distance based on species
arcpy.CalculateField_management(tempFC, "Buff_Dist", "buffDist(!LASTSPECIES!)", "PYTHON", codeblock)
print("Calculated the buffer distance for each nest according to species")

# Buffer the raptor nests, using the buffer distance field
arcpy.Buffer_analysis(tempFC, outputFC, "Buff_Dist")
print("Buffered the raptor nests")
print("Saved the output as: "+outputFC)

# Add message listing which features were not buffered
try:
    with arcpy.da.SearchCursor(tempFC, ['NestIDCode','Buff_Dist'],'"Buff_Dist"=0') as cursor:
        for row in cursor:
            print('Nest {0} was not buffered'.format(row[0]))
except:
    pass

# Delete the temporary feature class
arcpy.Delete_management(tempFC)
print("Deleted the temporary feature class")

print("All done!")

