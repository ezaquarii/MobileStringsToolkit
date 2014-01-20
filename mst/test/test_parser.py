'''
Created on 19-05-2013

@author: tn
'''
from mst.spreadsheet import Spreadsheet
from mst.test.reference import Spreadsheet as reference
import csv
import unittest

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