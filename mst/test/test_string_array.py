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
from mst.resources import StringArray
from mst.exceptions import MstException

def build_test_string(lang):
    return 'test %s' % lang

class TestStringArrayCreation(unittest.TestCase):
    
    def testKeyCanBeAssignedOnlyOne(self):
        key = "key"
        string_array = StringArray(key, [])
        self.assertEqual(string_array.key, key)
        try:
            string_array.key = "different key"
            self.fail("This operation should fail")
        except AttributeError:
            pass
        
    def testKeyMustBeAString(self):
        keys = [ object(), [], {}, () ]
        for key in keys:
            try:
                string_array = StringArray(key, [])
                self.fail("This operation should fail")
            except ValueError:
                pass

class TestStringArrayAdd(unittest.TestCase):

    valid_languages = set(['en', 'fr'])
    invalid_languages = set(['de', 'es'])

    def testArrayContainsProvidedLanguages(self):
        string_array = StringArray('key', self.valid_languages)
        self.assertEqual( self.valid_languages, string_array.languages )
        
    def testAddWithValidLanguageSucceed(self):
        string_array = StringArray('key', self.valid_languages)
        for index in range(0,3):
            for lang in self.valid_languages:
                text = build_test_string(lang)
                string_array.add(lang, index, text )
                self.assertEqual( text, string_array.get(lang, index) )   # get added item
                self.assertEqual( string_array.size(lang), index+1)       # check array size
                
    def testAddWithInvalidLanguageFails(self):
        string_array = StringArray('key', self.valid_languages)
        for index in range(0,3):
            for lang in self.invalid_languages:
                text = build_test_string(lang)
                try:
                    string_array.add(lang, index, text )
                    self.fail('Operation should fail for language %s' % lang)
                except MstException:
                    pass


class TestStringArrayMerge(unittest.TestCase):
    
    def __build_test_string(self, lang, index):
        return ( 'text %s %s' % (lang, index) )
    
    def setUp(self):
        self.languages = ['en', 'fr']
        self.arrays = {}
        for lang in self.languages:
            self.arrays[lang] = {}
            for index in range(0,3):
                self.arrays[lang][index] = self.__build_test_string(lang, index);
    
    def testMergeWithDifferentKeysFail(self):
        array1 = StringArray('key a', ['en'])
        array2 = StringArray('key b', ['fr'])
        try:
            array1.merge(array2)
            self.fail('This operation should fail')
        except MstException:
            pass
    
    def testMergeWithSameLanguagesFail(self):
        array1 = StringArray('key', ['en', 'fr'] )
        array2 = StringArray('key', ['en', 'de'] )
        try:
            array1.merge(array2)
            self.fail('This operation should fail')
        except MstException:
            pass        
    
    def testMergeSuccess(self):
        arrays = []
        max_items = 10
        # create independend string arrays
        for lang in self.languages:
            array = StringArray('key', [lang])
            for index in range(0,max_items):
                array.add(lang, index, self.__build_test_string(lang, index))
            arrays.append(array)
        
        # check all items contain proper number of items for each language
        for array in arrays:
            for lang in array.languages:
                self.assertEqual( array.size(lang), max_items )
        
        # create empty string array
        merged = StringArray('key', [])
        
        # merge all arrays
        for array in arrays:
            merged.merge(array)
        
        # check if resulting array contains all languages from all merged items
        combined_languages = set()
        for array in arrays:
            combined_languages.update( array.languages )
        self.assertEqual( combined_languages, merged.languages )
        
        # check if merged item contain proper number of items for each language        
        for lang in merged.languages:
            self.assertEqual( merged.size(lang), max_items ) 
    
    