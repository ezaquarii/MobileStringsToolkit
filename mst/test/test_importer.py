'''
Created on 13-07-2013

@author: tn
'''
import unittest
import os
from mst import Config
from mst.importer import AndroidImporter
from mst.test.reference import AndroidImporter as reference
from xml.etree import ElementTree as etree

class TestImporterAndroid(unittest.TestCase):

    def _load_resources(self, language,  load_resources_method):
        """
        Use AndroidImporter object and load resources from XML files.
        It calls load_resources_method on an AndroidImporter object,
        passing language and parsed XML tree. Param load_resources_method
        is one of:
        
        * AndroidImporter._load_strings
        * AndroidImporter._load_string_arrays
        * AndroidImporter._load_quantity_strings
        
        Return a dictionary mapping language codes to resource arrays.
        """
        
        imp = AndroidImporter()
        xml_file_path = self.config.resource_file_path(language)
        xml_file = open(xml_file_path)
        xml_tree = etree.parse(xml_file)
        if load_resources_method == AndroidImporter._load_strings:
            return imp._load_strings(language, xml_tree)
        elif load_resources_method == AndroidImporter._load_string_arrays:
            return imp._load_string_arrays(language, xml_tree)
        elif load_resources_method == AndroidImporter._load_quantity_strings:
            return imp._load_quantity_strings(language, xml_tree)
        else:
            self.fail("This method is not allowed: %s" % load_resources_method)
    
    def setUp(self):
        """
        Initialize configuration data used in all other tests.
        """
        # load project config
        self.config = Config(reference.project_root_path, False, reference.config_file_path)
        # check if root directory exists
        self.assertTrue( os.path.isdir( self.config.root ) )
        # check if all XML files exist
        for language in self.config.languages:
            filename = self.config.resource_file_path(language)
            self.assertTrue( os.path.isfile(filename) )
    
    def testLoadResourcesHelperFunctionWorks(self):
        for language in self.config.languages:
            strings = self._load_resources(language,  AndroidImporter._load_strings)
            arrays = self._load_resources(language,  AndroidImporter._load_string_arrays)
            quantity = self._load_resources( language,  AndroidImporter._load_quantity_strings)
            self.assertTrue( len(strings) > 0 )
            self.assertTrue( len(arrays) > 0 )
            self.assertTrue( len(quantity) > 0 )
    
    def testLoadsAllStringsForAllLanguages(self):
        for language in self.config.languages:
            strings = self._load_resources( language,  AndroidImporter._load_strings )
            self.assertEqual( len(strings), reference.string_count[language] )
    
    def testLoadsAllStringArraysForAllLanguages(self):
        for language in self.config.languages:
            arrays = self._load_resources( language,  AndroidImporter._load_string_arrays )
            self.assertEqual( len(arrays),  reference.string_array_count[language] )
            
    def testLoadsAllQuantityStringsForAllLanguages(self):
        for language in self.config.languages:
            arrays = self._load_resources( language,  AndroidImporter._load_quantity_strings )
            self.assertEqual( len(arrays),  reference.quantity_strings_count[language] )


