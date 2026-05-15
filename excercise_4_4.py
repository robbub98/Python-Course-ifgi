# Python in QGIS and ArcGIS
# HW 4: Group 8; Shiyar Murad & Robert Bartram

# Excercise 4.4

# Import package 'processing'
import processing

# Full paths to shapefiles 'Schools' and 'Muenster_City_Districts'
schools = r"/Users/robbub/Documents/UniMünster/SoSe26/PIGIS/Python_Course_ifgi/excercise_4/Muenster/Schools.shp"
districts = r"/Users/robbub/Documents/UniMünster/SoSe26/PIGIS/Python_Course_ifgi/excercise_4/Muenster/Muenster_City_Districts.shp"

# Run function 'countpointsinpolygon'
result = processing.run("qgis:countpointsinpolygon", {
    'POINTS': schools,
    'POLYGONS': districts,
    'WEIGHT': None,
    'OUTPUT': 'memory:'
})

# Read result and print result
output_layer = result['OUTPUT']

for feature in output_layer.getFeatures():
  # Get the list of attributes for the current feature
    attrs = feature.attributes()
    
    # Print the entry at index 3 and index 7
    print(attrs[3], ' :',attrs[7])
