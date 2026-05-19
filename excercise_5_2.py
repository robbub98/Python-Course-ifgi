# Python in QGIS and ArcGIS
# HW 5: Group 8; Shiyar Murad & Robert Bartram

# Excercise 5.2

# This script when running asks the user to enter coordinates, via a QMessageBox
# the user then should be informed, if the input falls into a district of Muenster

# ------------------------------------------------------------------------------
# Setup coordinate conversion from WGS-84 to UTM Zone 32 N coordinates

# Get 'Muenster_City_Districts' layer
city_districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# Define User input CRS
crs_from = QgsCoordinateReferenceSystem(4326)

# Define target CRS
crs_to = city_districts.crs()

# Create transformation object
transform = QgsCoordinateTransform(crs_from, crs_to, QgsProject.instance())


# ------------------------------------------------------------------------------
# Setup a QInputDialog window to enter coordinates

parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(
    parent,
    "Coordinates", 
    "Enter coordinates as latitude, longitude",
    text = "51.96066,7.62476"
)


# ------------------------------------------------------------------------------
# parse and convert input string into numerical longitude and latitude values

if bOk:
    parts = sCoords.split(",") # split string after the comma
    lat = float(parts[0]) # north-south
    lon = float(parts[1]) # east-west
    
    # QgsPointXY(x, y) = QgsPointXY(longitude, latitude)
    point_wgs84 = QgsPointXY(lon, lat)
    
    # Transform to the layer's CRS
    point_projected = transform.transform(point_wgs84)
    
    # Wrap in a QgsGeometry so we can use .within()
    point_geom = QgsGeometry.fromPointXY(point_projected)


# ------------------------------------------------------------------------------
# Check whether coordinates fall into a district of Muenster 
# and inform user via QMessageBox

found = False

for district in city_districts.getFeatures():
    district_geom = district.geometry()
    
    if point_geom.within(district_geom):
        district_name = district["Name"]
        QMessageBox.information(
            parent,
            "Spot on!",
            f"The point lies within: {district_name}"
        )
        found = True
        break 
        
if not found:
    QMessageBox.information(
        parent,
        "Miss!",
        "Your point does not lie in Muenster"
    )