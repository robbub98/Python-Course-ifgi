# Python in QGIS and ArcGIS
# HW 5: Group 8; Shiyar Murad & Robert Bartram

# Excercise 5.1

# This script opens a dropdown menu with all the city disctricts of Muenster
# ordered alphabetically. When choosing a district on click, it shows the 
# existing schools in the district.

# ------------------------------------------------------------------------------
# setup QDistanceArea
da = QgsDistanceArea()
da.setEllipsoid('ETRS89')

print(districts.crs().authid())

da.setSourceCrs(districts.crs(), QgsProject.instance().transformContext())

# ------------------------------------------------------------------------------
# setup a dialog window with QInputDialog

# iface.mainWindow() gives dialogs a proper QGIS parent window
parent = iface.mainWindow()

# Get the city districts layer 
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# check if the layer was loaded correctly before doing anything else
if not districts.isValid():
    print("Layer failed to load!")

# ------------------------------------------------------------------------------
# build sorted district names list
districts_names =[]

# Build a request that returns features sorted alphabetically by Name
request = QgsFeatureRequest()
clause = QgsFeatureRequest.OrderByClause("Name")
request.setOrderBy(QgsFeatureRequest.OrderBy([clause]))

for district in districts.getFeatures(request):
    districts_names.append(district["Name"])

# ------------------------------------------------------------------------------
# show dropdown dialog window
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ", districts_names)

# ------------------------------------------------------------------------------
# check if user canceled 
if not bOk:
    QMessageBox.warning(parent, "Schools", "User cancelled")

# ------------------------------------------------------------------------------
# find selected districts geometry with .geometry()
# and compute centroid
if bOk:
    geom_district = None
    centroid = None
    for district in districts.getFeatures():
        if district["Name"] == sDistrict:
            geom_district = district.geometry()
            centroid = geom_district.centroid()
            break # stop as soon as we found it
  
# ------------------------------------------------------------------------------  
# find the schools in the selected districts with .within()
# select layer Schools
schools = QgsProject.instance().mapLayersByName("Schools")[0]

# build request that orders schools by 
school_request = QgsFeatureRequest()
school_clause = QgsFeatureRequest.OrderByClause("NAME")
school_request.setOrderBy(QgsFeatureRequest.OrderBy([school_clause]))

output = "" # setup output string for later use
school_ids = [] # collect IDs for selection + zoom later


for school in schools.getFeatures(school_request):
    if school.geometry().within(geom_district):
        
        # Get the school's coordinates as a QgsPointXY
        school_point = QgsPointXY(school.geometry().asPoint())
        
        
        # Get the centroid as a QgsPointXY
        centroid_point = QgsPointXY(centroid.asPoint())
        
        # measureLine() returns distance in metres — divide by 1000 for km
        distance_km = round(da.measureLine(school_point, centroid_point) / 1000, 2)
        
        # Add to output string
        output += f"{school['NAME']}, {school['SchoolType']} \nDistance to districtcentrum {distance_km} km\n\n"
        
        # Add school to selected features list
        school_ids.append(school.id())
 
#  ------------------------------------------------------------------------------ 
# show result, selet and zoom to schools in selected district

# Show the popup
QMessageBox.information(parent, f"Schools in {sDistrict}", output)

# Select the matching schools on the map
schools.selectByIds(school_ids)

# Zoom the map canvas to the selected schools
iface.mapCanvas().zoomToSelected(schools)

# Optional: if the zoom is too close, set a minimum scale
if iface.mapCanvas().scale() < 50000:
    iface.mapCanvas().zoomScale(50000)
