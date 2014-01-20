from xml.etree import ElementTree as etree
from mst.importer import AndroidImporter
from mst import QuantityStrings

xml = etree.parse( open('strings.xml') )

quantity_string_nodes = xml.findall( AndroidImporter.QUANTITY_STRINGS )

print("Loaded %s string arrays" % len(quantity_string_nodes) )
language = 'en'

resources = []
for quantity_strings in quantity_string_nodes:
    key = quantity_strings.attrib['name']
    resource = QuantityStrings(key,  [language])
    for item in quantity_strings.findall('item'):
        quantity = item.attrib['quantity']
        if quantity in QuantityStrings.QUANTITIES:
            resource.add_quantity_string(language,  quantity,  item.text)
    resources.append( resource )

