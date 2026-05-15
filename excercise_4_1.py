# Python in QGIS and ArcGIS
# HW 4: Group 8; Shiyar Murad & Robert Bartram

# excercise 4.1

# This is the code for a python action in QGIS that opens the wikipedia article
# to the clicked district of Muenster.

# to open a website and a pop-up window you need the two packages below
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# create new instance of QWebView
QWebView = QWebView(None)

# set the URL dynamically to the clicked polygon with [%Name%]
# and load URL for instance QWebView
QWebView.load(QUrl("https://en.wikipedia.org/wiki/[%Name%]"))

# display pop up window with created URL
QWebView.show() 