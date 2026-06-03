# Python in QGIS and ArcGIS
# HW 6: Group 8; Shiyar Murad & Robert Bartram

# Excercise 6.2

# This script makes changes to the layer 'public_swimming_pools', it completes
# the full name of type of swimming pool and adds the district value to each 
# item in the layer.

# Step 1: Load layers 'public_swimming_pools' and 'Muenster_City_Districts'

pools = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# Step 2: Check capabilities before making changes

provider = pools.dataProvider()
capabilities = provider.capabilitiesString()
print(capabilities) # useful to see what's available
if "Objekte hinzufügen" in capabilities:
    print("We can add fields.")
else:
    print("This layer does not support adding fields.")
    
# Step 3: Add new 'district' field (only if it doesn't exist yet)
if "Objekte hinzufügen" in capabilities:
    # Check if field "district" already exists to avoid duplicates
    if pools.fields().indexOf("district") == -1:
        new_field = QgsField("district", QVariant.String, "string", 50)
        provider.addAttributes([new_field])
        pools.updateFields()
        print("Field 'district' added.")
    else:
        print("Field 'district' already exists, skipping addition.")
    
# Step 4: loop through 'public_swimming_pools' and add data

fields = pools.fields()

if "Attributwerte ändern" in capabilities:
    for pool in pools.getFeatures():
        pool_id = pool.id()
        pool_geom = pool.geometry()

        # Translate the type letter
        # preventing when running script second time Type is not overwritten
        current_type = pool["Type"]
        if current_type == "H":
            new_type = "Hallenbad"
        elif current_type == "F":
            new_type = "Freibad"
        else:
            new_type = current_type
    
        # Build the change dictionary — keys are field indexes
        attributes = {
            fields.indexOf("Type"): new_type
        }

        # Find which district this pool is in
        for district in districts.getFeatures():
            if pool_geom.within(district.geometry()):
                attributes[fields.indexOf("district")] = district["Name"]
                break # a pool can only be in one district
    
        # Write all changes for this feature in one call
        provider.changeAttributeValues({pool_id: attributes})

print("Processing complete!")