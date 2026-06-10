"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from typing import Any, Optional
import os

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProject,
    QgsFeatureRequest,
    QgsDistanceArea,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsUnitTypes,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsVectorLayer,
    QgsFeature,
    QgsSimpleFillSymbolLayer,
    QgsFillSymbol,
    QgsSingleSymbolRenderer,
    QgsRasterLayer # <-- NEW IMPORT REQUIRED FOR OSM
)
from qgis.PyQt.QtCore import QCoreApplication, QSize, Qt
from qgis.PyQt.QtGui import QImage, QPainter

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader


# Class CreateCityDistrictProfile - Processing Tool to create Profile of one
# city district in Muenster.

class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    
    # Parameter key constants 
    
    city_districts = "CITY_DISTRICTS"
    choice_layer = "CHOICE_LAYER"
    pdf_output = "PDF_OUTPUT"
    
    # Identity methods

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)
    
    def createInstance(self):
        return CreateCityDistrictProfile()
    
    def name(self):
        return 'createcitydistrictprofile'
    
    def displayName(self):
        return self.tr('Create City District Profile')
    
    def group(self):
        return self.tr('City District Tools')
    
    def groupId(self):
        return 'citydistricttools'
    
    def shortHelpString(self):
        return self.tr("Creates a PDF profile for a selected Münster citydistrict.")

    
    # Helper methods
    
    # getCityDistrictList() - method to extract City district names and sorts
    # them alphabetically in a list
    
    def getCityDistrictList(self):
        
        layers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
        if not layers:
            return ["Please load 'Muenster_City_Districts' layer first"]
            
        districts = layers[0]
        
        names = []
        
        if districts.isValid:
            request = QgsFeatureRequest()
            clause = QgsFeatureRequest.OrderByClause("NAME")
            request.setOrderBy(QgsFeatureRequest.OrderBy([clause]))
            
            for district in districts.getFeatures(request):
                names.append(district["NAME"])
            
        return names

    # CreateStatistics() does the spatial analysis for the pdf file
    
    def createStatistics(self, cityDistrictName, chosenLayer, feedback):
        
        # Pt.1: It loads all the layers and filters the data according to the
        # users choices from the GUI window
        
        districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        houseNums = QgsProject.instance().mapLayersByName("House_Numbers")[0]
        parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]
        
        if chosenLayer == "Schools":
            pointLayer = QgsProject.instance().mapLayersByName("Schools")[0]
        else:
            pointLayer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
                
        
        # Filter districts layer to find chosen layer from user
        request = QgsFeatureRequest()
        request.setFilterExpression(f'"Name" = \'{cityDistrictName}\'')
        
        district_geom = None
        parent_district = ""
        
        for district in districts.getFeatures(request):
            district_geom = district.geometry()
            parent_district = district["P_District"]
            district_id = district.id()
            break
            
        if not district_geom:
            raise QgsProcessingException("District geometry not found.")
        
    # Pt.2: Here it does the calculation of the area of the district
        # Uses QgsDistanceArea with the correct ellipsoid — gives accurate realworld measurements
        
        da = QgsDistanceArea()
        da.setEllipsoid('ETRS89')
        
        # measureArea() returns square metres — divide twice by 1000 to get km²
        area_km2 = round(da.measureArea(district_geom) / 1000 / 1000, 2)
        
    # Pt.3: This code section counts the features within the district from the layer
      
        bbox_request = QgsFeatureRequest().setFilterRect(district_geom.boundingBox())
        
        feedback.pushInfo("Counting houses...")
        count_houses = sum(1 for h in houseNums.getFeatures(bbox_request) if h.geometry().within(district_geom))
    
        feedback.pushInfo(f"Counting {chosenLayer.lower()}...")
        count_choice = sum(1 for f in pointLayer.getFeatures(bbox_request) if f.geometry().within(district_geom))
    
        feedback.pushInfo("Counting parcels...")
        count_parcels = sum(1 for p in parcels.getFeatures(bbox_request) if p.geometry().intersects(district_geom))
    
    # Pt. 4: Create Snapshot of Map for chosen District
        feedback.pushInfo("Generating map image...")
        image_path = os.path.join(QgsProject.instance().homePath(), "temp_map.png")
        
        # Include OSM background map view for better orientation in map snapshot
        osm_uri = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
        osm_layer = QgsRasterLayer(osm_uri, "OSM", "wms")
        
        # Create a temporary highlight layer for the chosen district
        highlight_layer = QgsVectorLayer(f"Polygon?crs={districts.crs().authid()}", "highlight", "memory")
        prov = highlight_layer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(district_geom)
        prov.addFeatures([feat])
        
        # Style the highlight layer (Red outline, light red semi-transparent fill)
        symbol_layer = QgsSimpleFillSymbolLayer.create({
            "color": "255,0,0,50",          # 50 is alpha (transparency)
            "outline_color": "255,0,0,255", # Solid red border
            "outline_width": "0.8"
        })
        symbol = QgsFillSymbol.createSimple({})
        symbol.changeSymbolLayer(0, symbol_layer)
        highlight_layer.setRenderer(QgsSingleSymbolRenderer(symbol))

        settings = QgsMapSettings()
        # Order layers correctly and change CRS of OSM to layers CRS
        settings.setLayers([highlight_layer, districts, osm_layer])
        settings.setDestinationCrs(districts.crs())
        settings.setBackgroundColor(Qt.white)
        
        # Set size of map snapshot dynamically
        
        extent = district_geom.boundingBox()
        extent.scale(1.15)
        settings.setExtent(extent)
        
        aspect_ratio = extent.width() / extent.height()
        img_width = 800
        img_height = int(img_width / aspect_ratio)
        
        settings.setOutputSize(QSize(img_width, img_height))
        
        image = QImage(QSize(img_width, img_height), QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.white)
        painter = QPainter(image)
        job = QgsMapRendererCustomPainterJob(settings, painter)
        job.start()
        job.waitForFinished()
        painter.end()
        image.save(image_path)
        
    # Pt. 5: Create Dict with relevant information for creation of pdf
    
        return {
            "parent_district": parent_district,
            "area_km2": area_km2,
            "count_houses": count_houses,
            "count_parcels": count_parcels,
            "chosen_layer": chosenLayer,
            "count_choice": count_choice,
            "image_path": image_path
        }
    
    # Method createPDF() for creating the pdf with all the information
    
    def createPDF(self, cityDistrict, layerChoice, pdf_output, feedback):
        # Get data from createStatistics()
        data = self.createStatistics(cityDistrict, layerChoice, feedback)
        
        # Set up the PDF document and styles
        pdf = SimpleDocTemplate(pdf_output)
        styles = getSampleStyleSheet()
        page_width, _ = letter
        content = []
        
        # Title
        content.append(Paragraph(f"City District Profile: {cityDistrict}",
        styles["Title"]))
        content.append(Spacer(1, 12))
        
        # Map image of the district
        img_reader = ImageReader(data["image_path"])
        img_w, img_h = img_reader.getSize()
        aspect = img_h / float(img_w)
        
       # Make the image take up 70% of the page width, scale height automatically
        draw_width = page_width * 0.7 
        draw_height = draw_width * aspect 
        
        map_img = Image(data["image_path"], width=draw_width, height=draw_height)
        content.append(map_img)
        content.append(Spacer(1, 12))
        
        # Features all the profile information for district
        no_feature_msg = f"No {data['chosen_layer'].lower()} in this district."
        feature_msg = f"{data['count_choice']} {data['chosen_layer'].lower()} are located here."
        
        body = f"""
        The district {cityDistrict} is part of the parent district {data['parent_district']}.
        It covers an area of {data['area_km2']} km² and contains {data['count_parcels']} parcels
        with a total of {data['count_houses']} registered addresses.
        
        """ + (f"{feature_msg}" if data["count_choice"] > 0 else no_feature_msg)
        
        content.append(Paragraph(body, styles["Normal"]))
        content.append(Spacer(1, 12))
        
        # Build and save the PDF
        pdf.build(content)
        
        # Clean up the temporary map image
        os.remove(data["image_path"])
        
    # initAlgorithm method

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
    
        # Dropdown for choosing City Districts
        
        self.addParameter(
            QgsProcessingParameterEnum(
                "CITY_DISTRICTS",
                "Choose a city district",
                options = self.getCityDistrictList(),
                usesStaticStrings = True
            )
        )
    
        # Binary checkbox for Schools or Pools
        
        self.addParameter(
            QgsProcessingParameterEnum(
                "CHOICE_LAYER",
                "Include statistics for:",
                options = ["Schools", "Pools"],
                usesStaticStrings = True
            )
        )

        # Dropdown menu for choosing file path for saving pdf
    
        self.addParameter(
            QgsProcessingParameterFileDestination(
                "PDF_OUTPUT",
                self.tr("Output PDF file"),
                fileFilter = "PDF files (*.pdf)"
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        # Read each GUI value using the matching parameterAs…() method
        city_district = self.parameterAsString(parameters, "CITY_DISTRICTS", context)
        layer_choice = self.parameterAsString(parameters, "CHOICE_LAYER", context)
        pdf_path = self.parameterAsFileOutput(parameters, "PDF_OUTPUT", context)
        
        # Run the whole pipeline
        self.createPDF(city_district, layer_choice, pdf_path, feedback)
        
        # Always return a dict matching your output parameter keys
        return {"PDF_OUTPUT": pdf_path}
        
        
        