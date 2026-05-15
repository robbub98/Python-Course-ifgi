# Python in QGIS and ArcGIS
# HW 4: Group 8; Shiyar Murad & Robert Bartram

# Excercise 4.3

# This code creates a new QGIS project from VS code that loads all shapefiles as layers 
# into the project that exist in the folder

import os
from qgis.core import QgsProject, QgsVectorLayer

# Path to münster folder
folder_path = r'C:\Pythonn\S04\Muenster\Muenster'

# Create a new QGIS project and remove all the exiciting layers
project = QgsProject.instance()
project.removeAllMapLayers()

# Create an empty list to store the shapefile
shapefiles = []

# Read all the files in the folder
for file in os.listdir(folder_path):

    # Check if the file is a shapefile
    if file.endswith('.shp'):

        # Create the full file path
        ful_path = os.path.join(folder_path, file)

        # Add the path to the list
        shapefiles.append(full_path)

# Loop through all shapefiles
for shp in shapefiles:

    #Create a vector layer from the shapefile
    layer = QgsVectorLayer(shp, os.path.basename(shp).replace('.shp', ''), 'ogr')

    # Check if the layer is valid
    if layer.isValid():
        # Add the layer to the project
        project.addMapLayer(layer)

# Save the project to a file
project.write(r'C:\Pythonn\S04\Muenster\Muenster\myFirstProject.qgz')
