# Python in QGIS and ArcGIS
# HW 6: Group 8; Shiyar Murad & Robert Bartram

# Excercise 6.1

# This script creates a new layer  from scratch called '
# temp_standard_land_value_muenster', using a .csv file.


# Step 1: Identifying path for .csv file and reading lines

import os

# Browsing for folder where script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

# Building path to the CSV folder inside the directory
file_path = os.path.join(script_dir, "Data for Session 6", "standard_land_value_muenster.csv")

# Using 'with' automatically closes the file for you
with open(file_path, "r") as csv_file:
    lines = csv_file.readlines()

# Have a peek at what the data looks like
# .strip() removes the \n at the end of the line for cleaner printing
print(lines[0].strip()) # header row
print(lines[1].strip()) # first data row

# Step 2: Create memory layer 

# Set uri string
uri = ("polygon?"
    "crs=EPSG:25832&"
    "field=standard_land_value:double&"
    "field=type:string&"
    "field=district:string")

# Use direct approach with provider to create new layer 'temp_standard_land_value_muenster'
layer = QgsVectorLayer(uri, "temp_standard_land_value_muenster", "memory")
provider = layer.dataProvider()

# Step 3: Loop and parse each row

# Use lines[1:] to skip the header row
for line in lines[1:]:
    # Split line into a list of strings based on the semicolon
    parts = line.split(";")
    
    # Parse the data
    # parts[0] is the land value, parts[1] is type, parts[2] is district
    
    # handle commas in float with changing it to point
    land_value = float(parts[0].replace(",", "."))
    land_type = parts[1]
    district = parts[2]
    
    # The WKT is the last column — strip (\n)
    wkt = parts[3].strip()
    
    # Convert WKT string to a QgsGeometry object
    geom = QgsGeometry.fromWkt(wkt)
    
    # Build the feature using the layer's field definitions
    feat = QgsFeature(layer.fields())
    feat.setAttribute("standard_land_value", land_value)
    feat.setAttribute("type", land_type)
    feat.setAttribute("district", district)
    feat.setGeometry(geom)
    
    # Add the feature to the provider
    provider.addFeatures([feat])
    
# Step 4: Add new layer to map

# This adds the layer to the QGIS Table of Contents
QgsProject.instance().addMapLayer(layer)
