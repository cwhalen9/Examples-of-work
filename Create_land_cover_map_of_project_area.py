"""
GEOG 485
Final Project
Cara Whalen
July 2020
"""

import os
import arcpy
import csv
arcpy.env.overwriteOutput = True

# Define the workspace
arcpy.env.workspace = r"C:\PSU\Geog485\FinalProject\Shapefiles"

# Input variables
boundaryInput = r"Tool_Inputs\ProjectBoundary.shp"
projectName = "Example Project"
spatialRef = arcpy.SpatialReference(26913)  #NAD 1983 utm zone 13N
landcover = r"Tool_Inputs\NLCD_Landcover_Colorado.shp"

# Outputs
boundaryOutput = r"Tool_Outputs\ProjectBoundary_projected.shp"
landcoverClipped = r"Tool_Outputs\NLCD_clipped.shp"
landcoverProjectArea = r"Tool_Outputs\NLCD_clipped_projected.shp"
landcoverProjectAreaDiss = r"Tool_Outputs\NLCD_clipped_projected_dissolved.shp"
outputCSV = projectName.replace(" ", "") + "_landcover.csv"
projectPoint = r"Tool_Outputs\ProjectPoint.shp"

# Check the spatial reference of the input project boundary
boundarySpatialRef = arcpy.Describe(boundaryInput).spatialReference

# Project the project boundary file if needed
try:
    if boundarySpatialRef == "Unknown":
        boundaryOutput = arcpy.DefineProjection_management(boundaryInput, spatialRef)
        print "The spatial reference of the project boundary shapefile has been defined."
    elif boundarySpatialRef == spatialRef:
        boundaryOutput = boundaryInput
        print "The project boundary shapefile is in the correct spatial reference."
    else:
        arcpy.Project_management(boundaryInput, boundaryOutput, spatialRef)
        print "The project boundary shapefile has been projected to the correct spatial reference."
except:
    print "There was a problem projecting the boundary file."
    print arcpy.GetMessages()

# Clip the land cover to the project boundary
try:
    arcpy.Clip_analysis(landcover, boundaryOutput, landcoverClipped)
    print "The land cover has been successfully clipped to the project boundary."
except:
    print "There was a problem clipping the land cover to the project boundary."
    print arcpy.GetMessages()

# Check the spatial reference of the land cover and project if needed
try:
    landcoverSpatialRef = arcpy.Describe(landcoverClipped).spatialReference
    if landcoverSpatialRef == "Unknown":
        landcoverProjectArea = arcpy.DefineProjection_management(landcoverClipped, spatialRef)
        print "The spatial reference of the landcover shapefile has been defined."
    elif landcoverSpatialRef == spatialRef:
        landcoverProjectArea = landcoverClipped
        print "The landcover shapefile is in the correct spatial reference."
    else:
        arcpy.Project_management(landcoverClipped, landcoverProjectArea, spatialRef)
        print "The landcover shapefile has been projected to the correct spatial reference."
except:
    print "There was a problem projecting the land cover shapefile."
    print arcpy.GetMessages()

# Dissolve the clipped land cover
try:
    arcpy.Dissolve_management(landcoverProjectArea, landcoverProjectAreaDiss, "gridcode")
    print "The clipped land cover shapefile has been dissolved to land cover type."
except:
    print "There was a problem dissolving the land cover shapefile."
    print arcpy.GetMessages()

# Add a field for the land cover names
try:
    arcpy.AddField_management(landcoverProjectAreaDiss, "landcover", "TEXT")
    print "A new field has been added for the land cover names."
except:
    print "There was a problem adding a new field for the land cover names."
    print arcpy.GetMessages()

# Populate the new field with the land cover names
try:
    with arcpy.da.UpdateCursor(landcoverProjectAreaDiss, ["gridcode", "landcover"]) as cursor:
        for row in cursor:
            if row[0] == 11:
                row[1] = "Open Water"
            elif row[0] == 12:
                row[1] = "Perennial Ice/Snow"
            elif row[0] == 21:
                row[1] = "Developed, Open Space"
            elif row[0] == 22:
                row[1] = "Developed, Low Intensity"
            elif row[0] == 23:
                row[1] = "Developed, Medium Intensity"
            elif row[0] == 24:
                row[1] = "Developed High Intensity"
            elif row[0] == 31:
                row[1] = "Barren Land (Rock/Sand/Clay)"
            elif row[0] == 41:
                row[1] = "Deciduous Forest"
            elif row[0] == 42:
                row[1] = "Evergreen Forest"
            elif row[0] == 43:
                row[1] = "Mixed Forest"
            elif row[0] == 51:
                row[1] = "Dwarf Scrub"
            elif row[0] == 52:
                row[1] = "Shrub/Scrub"
            elif row[0] == 71:
                row[1] = "Grassland/Herbaceous"
            elif row[0] == 72:
                row[1] = "Sedge/Herbaceous"
            elif row[0] == 73:
                row[1] = "Lichens"
            elif row[0] == 74:
                row[1] = "Moss"
            elif row[0] == 81:
                row[1] = "Pasture/Hay"
            elif row[0] == 82:
                row[1] = "Cultivated Crops"
            elif row[0] == 90:
                row[1] = "Woody Wetlands"
            elif row[0] == 95:
                row[1] = "Emergent Herbaceous Wetlands"
            cursor.updateRow(row)    
    del cursor
    print "The new field has been populated with the names of each land cover type."
except:
    print "There was a problem populating the new field with the land cover names."
    print arcpy.GetMessages()

# Add a field for the area
try:
    arcpy.AddField_management(landcoverProjectAreaDiss, "acres", "FLOAT")
    print "A new field has been added for the acres."
except:
    print "There was a problem adding a new field for the acres."
    print arcpy.GetMessages()

# Calculate the acerage of each land cover type
try:
    with arcpy.da.UpdateCursor(landcoverProjectAreaDiss, ["SHAPE@AREA", "acres"]) as cursor:
        for row in cursor:
            row[1] = row[0]/4047
            cursor.updateRow(row)    
    del cursor
    print "The acreage of each land cover type has been calculated."
except:
    print "There was a problem calculating the land cover acreages."
    print arcpy.GetMessages()

# Export the land cover acreages to a csv file
try:
    with open(outputCSV, "w") as csvfile:  
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')  
        fields = ['gridcode','landcover','acres']  
        csvwriter.writerow(fields)  
        with arcpy.da.SearchCursor(landcoverProjectAreaDiss, fields) as cursor:  
            for row in cursor:  
                csvwriter.writerow(row)
    del cursor
    print "The land cover acreages have been exported to a CSV file."
except:
    print "There was a problem exporting the CSV file."
    print arcpy.GetMessages()

# Open map document template
try:
    templatedoc = arcpy.mapping.MapDocument("Map_Template.mxd")
    print "The map document template has been opened."
except:
    print "There was a problem opening the map template file."
    print arcpy.GetMessages()

# Save template as new map document
try:
    templatedoc.saveACopy(projectName.replace(" ", "") + ".mxd")
    mapdoc = arcpy.mapping.MapDocument(projectName.replace(" ", "") + ".mxd")
    print "The map document template has been saved as a new mxd."
except:
    print "There was a problem saving a copy of the map template file."
    print arcpy.GetMessages()
    
# List the data frames
try:
    dfList = arcpy.mapping.ListDataFrames(mapdoc)
    mainDF = dfList[0]
    insetDF = dfList[1]
    print "The data frames have been identified."
except:
    print "There was a problem listing the data frames."
    print arcpy.GetMessages()

# Add clipped land cover and project boundary shapefiles to the map
try:
    landcoverLayer = arcpy.mapping.Layer(landcoverProjectAreaDiss)
    arcpy.mapping.AddLayer(mainDF, landcoverLayer)
    boundaryLayer = arcpy.mapping.Layer(boundaryOutput)
    arcpy.mapping.AddLayer(mainDF, boundaryLayer)
    print "The land cover and project boundary shapefiles have been added to the map."
except:
    print "There was a problem adding the land cover and project boundary shapefiles to the map."
    print arcpy.GetMessages()

# Zoom to project boundary
try:
    mainDF.zoomToSelectedFeatures()
    print "The map has zoomed to the added features."
except:
    print "There was a problem zooming the map."
    print arcpy.GetMessages()

# Symbolize the landcover layer
try:
    landcoverMapLayer = arcpy.mapping.ListLayers(mapdoc, "", mainDF)[1]
    sourceLayer = arcpy.mapping.Layer("LandcoverSymbology.lyr")
    arcpy.mapping.UpdateLayer(mainDF,landcoverMapLayer,sourceLayer, True)
    print "The land cover has been symbolized."
except:
    print "There was a problem symbolizing the land cover."
    print arcpy.GetMessages()

# Symbolize the project boundary layer
try:
    boundaryMapLayer = arcpy.mapping.ListLayers(mapdoc, "", mainDF)[0]
    sourceLayer = arcpy.mapping.Layer("BoundarySymbology.lyr")
    arcpy.mapping.UpdateLayer(mainDF,boundaryMapLayer,sourceLayer, True)
    print "The project boundary has been symbolized."
except:
    print "There was a problem symbolizing the project boundary."
    print arcpy.GetMessages()

# Rename the project boundary layer
boundaryMapLayer.name = "Project Area"

# Create point at center of project boundary polygon
try:
    with arcpy.da.SearchCursor(boundaryOutput, "SHAPE@XY") as cursor:
        centroid_coords = []
        for feature in cursor:
            centroid_coords.append(feature[0])
    del cursor

    point = arcpy.Point()
    pointGeometryList = []

    for pt in centroid_coords:
        point.X = pt[0]
        point.Y = pt[1]

        pointGeometry = arcpy.PointGeometry(point)
        pointGeometryList.append(pointGeometry)

    arcpy.CopyFeatures_management(pointGeometryList, projectPoint)
    arcpy.DefineProjection_management(projectPoint, spatialRef)
    print "A point has been created at the center of the project polygon."
except:
    print "There was a problem creating the project center point."
    print arcpy.GetMessages()

# Add project point to inset map
try:
    projectPointLayer = arcpy.mapping.Layer(projectPoint)
    arcpy.mapping.AddLayer(insetDF, projectPointLayer)
    print "The project center point has been added to the inset map."
except:
    print "There was a problem adding the project center point to the inset map."
    print arcpy.GetMessages()

# Symbolize the project point in the inset map
try:
    updateLayer = arcpy.mapping.ListLayers(mapdoc, "", insetDF)[0]
    sourceLayer = arcpy.mapping.Layer("ProjectPointSymbology.lyr")
    arcpy.mapping.UpdateLayer(insetDF,updateLayer,sourceLayer, True)
    print "The project point has been symbolized."
except:
    print "There was a problem symbolizing the project point."
    print arcpy.GetMessages()

# Adjust the legend
try:
    legend = arcpy.mapping.ListLayoutElements(mapdoc,"LEGEND_ELEMENT")[0]
    legend.adjustColumnCount(2)
    legend.updateItem(landcoverMapLayer, "", "", True)
    print "The legend has been adjusted."
except:
    print "There was a problem adjusting the legend."
    print arcpy.GetMessages()

# Update the title
try:
    for item in arcpy.mapping.ListLayoutElements(mapdoc,"TEXT_ELEMENT"):
        if item.name == "Project Title":
            item.text = projectName
    print "The map title has been updated."
except:
    print "There was a problem updating the map title."
    print arcpy.GetMessages()

# Save the map document
mapdoc.save()
del mapdoc
del templatedoc
print "All done!"

