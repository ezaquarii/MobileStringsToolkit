from xml.etree import ElementTree as etree
from mst.importer import AndroidImporter

imp = AndroidImporter()

s = imp.load('en', 'strings.xml')
print(s)

