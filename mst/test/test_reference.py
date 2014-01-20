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

import unittest
from xml.etree import ElementTree as etree

class TestReferenceSpreadsheet(unittest.TestCase):
    
    def testCSVFileExists(self):
        """Try to load test CSV file """
        from mst.test.reference import Spreadsheet as reference
        open( reference.csv_file, 'r' )

class TestAndroidReferenceConfig(unittest.TestCase):

    def testAndroidReferenceConfigFileExists(self):
        """Try to load test config file"""
        from mst.test.reference import AndroidConfig as reference
        open( reference.config_file_path, 'r' )

class TestReferenceAndroidImporter(unittest.TestCase):
    """Test AndroidImporter reference data"""
    
    def testXmlPathsAreValid(self):
        """Load all XML files and try to parse them."""
        from mst.test.reference import AndroidImporter as reference
        for language in reference.languages:
            path = reference.xml_path(language)
            f = open( path, 'r' )
            xml_tree = etree.parse(f)
