#     This file is part of Mobile Strings Toolkit
#
#     Copyright (C) 2013 Krzysztof Narkiewicz <krzysztof.narkiewicz@ezaquarii.com>
#
#     Mobile Strings Toolkit is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
#     
#     Mobile Strings Toolkit is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with Mobile Strings Toolkit; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
from xml.etree import ElementTree as etree
from mst import String, StringArray, QuantityStrings

class Importer(object):
    pass


class AndroidImporter(Importer):

    STRING = 'string'
    STRING_ARRAY = 'string-array'
    STRING_ARRAY_ITEM = 'item'
    QUANTITY_STRINGS = 'plurals'

    def __init__(self):
        pass
    
    def _load_xml_files(self, files):
        """
        Load all XML files and parse them. Files is a dictionary { 'lang': 'path' }.
        """
        if not isinstance(files,  dict):
            raise TypeError("Dictionary language:path was expected, but got %s" % type(files) )
        xml_trees = {}
        for language in files.keys():
            path = files[language]
            f = open( path,  'r' )
            xml_trees[language] = etree.parse(f)
        return xml_trees
    
    def _load_strings(self, language, xml_tree):
        """
        Loads all string items from a parsed XML tree and returns a list of
        String resources which can be later merged together.
        """
        nodes = xml_tree.findall( AndroidImporter.STRING )
        resources = {}
        for node in nodes:
            key = node.attrib['name']
            text = node.text
            if isinstance( text, str ):
                resource = String(key, [language])
                resource.add(language, text)
                resources[key] = resource
        return resources
    
    def _load_string_arrays(self, language, xml_tree):
        """
        Loads all string array items from a parsed XML tree and
        returns a list of StringArray resources which can be later
        merged together.
        """
        string_array_nodes = xml_tree.findall( AndroidImporter.STRING_ARRAY )
        resources = {}
        for string_array in string_array_nodes:
            key = string_array.attrib['name']
            strings = []
            for item in string_array.findall( AndroidImporter.STRING_ARRAY_ITEM ):
                strings.append( item.text )
            resource = StringArray(key,  [language])
            for index in range(0,  len(strings) ):
                resource.add(language,  index,  strings[index])
            resources[key] = resource
        return resources

    
    def _load_quantity_strings(self, language, xml_tree):
        quantity_string_nodes = xml_tree.findall( AndroidImporter.QUANTITY_STRINGS )
        resources = {}
        for quantity_strings in quantity_string_nodes:
            key = quantity_strings.attrib['name']
            resource = QuantityStrings(key,  [language])
            for item in quantity_strings.findall('item'):
                quantity = item.attrib['quantity']
                if quantity in QuantityStrings.QUANTITIES:
                    resource.add_quantity_string(language,  quantity,  item.text)
            resources[key] = resource
        return resources
    
    def load(self, language, files):
        xml_trees = self._load_xml_files(files)
        for language in xml_trees.keys():
            xml_tree = xml_trees[language]
    


















