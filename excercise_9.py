## Excercise 9
## Python in QGIS and ArcGIS
## Group 8: Shiyar Murad & Robert Bartram

import arcpy

def process_assets():
    """
    Main function to consolidate active assets and create coverage buffers.
    """
    # Task 1: Setup
    arcpy.env.workspace = r"D:\python_course_ifgi\MyProject1\exercise_arcpy_1.gdb"
    arcpy.env.overwriteOutput = True

    # Task 2: Copy active points
    point_fcs = arcpy.ListFeatureClasses(feature_type="Point")
    fields = ["Shape@", "status", "type"]

    with arcpy.da.InsertCursor("active_assets", fields) as i_cur:
        for fc in point_fcs:
            if fc == "active_assets":
                continue
            with arcpy.da.SearchCursor(fc, fields, where_clause="status = 'active'") as s_cur:
                for row in s_cur:
                    i_cur.insertRow(row)

    # Task 3: Buffer by type
    sizes = {
        "mast": "300 Meters", 
        "mobile_antenna": "50 Meters", 
        "building_antenna": "100 Meters"
    }
    buffers = []

    for t, dist in sizes.items():
        lyr = f"lyr_{t}"
        # Create layer for each specific type
        arcpy.management.MakeFeatureLayer("active_assets", lyr, f"type = '{t}'")
        
        out = f"buf_{t}"
        arcpy.analysis.Buffer(lyr, out, dist)
        buffers.append(out)
    
    # Merge each specific layer into 'coverage' layer
    print("Merging buffers into coverage layer...")
    arcpy.management.Merge(buffers, "coverage")
    print("Process complete!")

# ENTRY POINT
if __name__ == "__main__":
    try:
        process_assets()
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(f"An error occurred: {e}")