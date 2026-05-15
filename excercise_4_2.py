# Python in QGIS and ArcGIS
# HW 4: Group 8; Shiyar Murad & Robert Bartram

# Excercise 4.2

# This code xports Name and coordinates from pointlayer 'Schools' to a CSV (semicolon‑separated)

import os
from qgis.core import QgsProject, QgsWkbTypes

# Path to the output file
output_path = r'/Users/robbub/Documents/UniMünster/SoSe26/PIGIS/Python_Course_ifgi/excercise_4/excercise_4_2.csv'

# Prepare the list that will hold every CSV line
lines = ["Name;X;Y"]                     # header line

#  Get the layer called 'Schools'
layer = QgsProject.instance().mapLayersByName('Schools')[0]

#  Loop over selected features
for feat in layer.getSelectedFeatures():
    # -----– retrieve the name of the school -----
    name = feat['NAME']

    # -----– extract the coordinates ---------------------------
    geom = feat.geometry()

    
    # Single‑point geometry
    pt = geom.asPoint()

    x = pt.x()
    y = pt.y()

    # -----– add a CSV line ------------------------------------
    lines.append(f"{name};{x:.6f};{y:.6f}")

# Write everything to the file
with open(output_path, "w", encoding="utf-8") as csv_file:
    csv_file.write("\n".join(lines))

print(f"CSV written to: {output_path}")
