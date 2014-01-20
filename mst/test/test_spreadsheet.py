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

from mst import Spreadsheet
from mst.test.reference import Spreadsheet as reference
import csv
import unittest
from mst.resources import QuantityStrings

class SpreadsheetTest(unittest.TestCase):
    
    def __test_spreadsheet(self):
        s = Spreadsheet('android_id', self.rows, reference.languages )
        return s
    
    def setUp(self):
        rows = []
        csv_file = open(reference.csv_file, 'r')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            rows.append(row)
        self.assertGreater(len(rows), 0, 'No rows loaded from reference CSV file')
        self.rows = rows

    def testHeaderParsedCorrectly(self):
        s = self.__test_spreadsheet()
        self.assertEqual(reference.type_column, s.type_column)
        self.assertEqual(reference.id_column, s.id_column )
        for lang in reference.languages:
            self.assertEqual( reference.language_columns[lang], s.language_column(lang) )
            
    def testDataIsNotEmpty(self):
        s = self.__test_spreadsheet()
        self.assertGreater( len(s.data), 0, 'Empty data set' )

    def testResourcesCanBeExtracted(self):
        s = self.__test_spreadsheet()
        strings = s.get_strings()
        arrays = s.get_string_arrays()
        quantities = s.get_quantity_strings()
        all = s.get_all_resources()
        self.assertEqual(len(strings), reference.string_rows )
        self.assertEqual(len(arrays), reference.string_array_resources )
        self.assertEqual(len(quantities), reference.quantity_strings_resources )
        self.assertEqual(len(all), reference.total_resources )
        
    def testOptionsForStringsAreParsed(self):
        sp = self.__test_spreadsheet()
        strings = sp.get_strings()
        for res in strings:
            for lang in res.languages:
                s = res.get(lang)
                self.assertEqual( s.options, reference.string_options ) 
                
    def testOptionsForStringArraysAreParsed(self):
        sp = self.__test_spreadsheet()
        arrays = sp.get_string_arrays()
        for res in arrays:
            for lang in res.languages:
                a = res.get_array(lang)
                for array_item, reference_option in zip( a, reference.string_array_options ):
                    self.assertEqual(array_item.options, [reference_option] )
                    
    def testOptionsForQuantityStringsAreParsed(self):
        sp = self.__test_spreadsheet()
        quantities = sp.get_quantity_strings()
        for res in quantities:
            for lang in res.languages:
                quantity_items = res.get_quantities(lang)
                for quantity, reference_option in zip( QuantityStrings.QUANTITIES, reference.quantity_strings_options ):
                    item = quantity_items[quantity]
                    self.assertEqual(item.options, [reference_option] )
