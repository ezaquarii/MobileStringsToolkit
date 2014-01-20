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
from mst.resources import QuantityStrings
from mst.exceptions import MstException

def build_test_text(lang):
    return ('text %s' % lang)

class TestQuantityStringCreation(unittest.TestCase):
    
    def testKeyCanBeAssignedOnlyOne(self):
        key = "key"
        string = QuantityStrings(key, [])
        self.assertEqual(string.key, key)
        try:
            string.key = "different key"
            self.fail("This operation should fail")
        except AttributeError:
            pass
        
    def testKeyMustBeAString(self):
        keys = [ object(), [], {}, () ]
        for key in keys:
            try:
                string = QuantityStrings(key, [])
                self.fail("This operation should fail")
            except ValueError:
                pass

class TestQuantityStringsAdd(unittest.TestCase):
     
    def setUp(self):
        self.proper_languages = ['en', 'fr']
        self.bad_languages = ['de', 'es']
 
    def testQuantityStringsContainAllQuantityKeys(self):
        string = QuantityStrings('key', self.proper_languages)
        for lang in self.proper_languages:
            quantities = string.get_quantities(lang)
            self.assertEqual( len(quantities), 6, "Expected 6 quantities")

    def testQuantityStringsAreEmptyByDefault(self):
        resource = QuantityStrings('key', self.proper_languages)
        for language in self.proper_languages:
            for quantity in QuantityStrings.QUANTITIES:
                value = resource.get_quantity_string(language, quantity)
                self.assertEqual(value, '', 'Expected quantity string %s for language %s to be empty' % (quantity, language) ) 

    def testAddTextForExistingLanguageSucceed(self):
        resource = QuantityStrings('key', self.proper_languages)
        for lang in self.proper_languages:
            text = build_test_text(lang)
            for quantity in QuantityStrings.QUANTITIES:
                resource.add_quantity_string(lang, quantity, text)
                self.assertEqual(resource.get_quantity_string(lang, quantity), text)
                
    def testAddTextForNonexistingLanguageFail(self):
        resource = QuantityStrings('key', self.proper_languages)
        for lang in self.bad_languages:
            for quantity in QuantityStrings.QUANTITIES:
                try:
                    quantity_string = build_test_text(lang)
                    resource.add_quantity_string(lang, quantity, quantity_string)
                    self.fail('This operation should fail')
                except MstException:
                    pass

    def testGetStringForNonexistingLanguageFail(self):
        resource = QuantityStrings('key', self.proper_languages)
        for lang in self.bad_languages:
            for quantity in QuantityStrings.QUANTITIES:
                try:
                    resource.get_quantity_string(lang, quantity)
                    self.fail('This operation should fail')
                except MstException:
                    pass
# 
# class TestStringMerge(unittest.TestCase):
#     
#     def setUp(self):
#         self.languages = ['en', 'fr']
#         self.texts = {}
#         for lang in self.languages:
#             self.texts[lang] = build_test_text(lang)
# 
#     def testMergeSucceeds(self):
#         strings = []
#         for lang in self.languages:
#             s = String('key', [ lang ] )
#             s.add( lang, build_test_text(lang) )
#             strings.append(s)
#         merged = String('key', [])
#         for s in strings:
#             merged.merge(s)
#         for lang in self.languages:
#             text = build_test_text(lang)
#             self.assertEqual(text, merged.get(lang) )
# 
#     def testMergeWithSameLanguagesFail(self):
#         string1 = String('key', self.languages )
#         string2 = String('key', [ self.languages[0] ] )
#         try:
#             string1.merge(string2)
#         except MstException:
#             pass
#             
#     def testMergeWithDifferentKeysFail(self):
#         string1 = String('key_a', self.languages )
#         string2 = String('key_b', self.languages )
#         try:
#             string1.merge(string2)
#         except MstException:
#             pass
