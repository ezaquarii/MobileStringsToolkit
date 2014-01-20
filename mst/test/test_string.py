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
import random
import string
from mst.resources import String
from mst.exceptions import MstException

def build_test_text(lang):
    return ('text %s' % lang)

class TestStringCreation(unittest.TestCase):
    
    def testKeyCanBeAssignedOnlyOne(self):
        key = "key"
        string = String(key, [])
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
                string = String(key, [])
                self.fail("This operation should fail")
            except ValueError:
                pass

class TestStringAdd(unittest.TestCase):
    
    def setUp(self):
        self.proper_languages = ['en', 'fr']
        self.bad_languages = ['de', 'es']

    def testDefaultStringsEmpty(self):
        string = String('key', self.proper_languages)
        for lang in self.proper_languages:
            text = string.get(lang)
            self.assertEqual(text, '')

    def testAddTextForExistingLanguageSucceed(self):
        string = String('key', self.proper_languages)
        for lang in self.proper_languages:
            text = build_test_text(lang)
            string.add(lang, text)
            self.assertEqual( text, string.get(lang) )
    
    def testAddTextForNonexistingLanguageFail(self):
        string = String('key', self.proper_languages)
        for lang in self.bad_languages:
            try:
                text = build_test_text(lang)
                string.add(lang, text)
                self.fail('This operation should fail')
            except MstException:
                pass

    def testGetStringForNonexistingLanguageFail(self):
        string = String('key', self.proper_languages)
        for lang in self.bad_languages:
            try:
                string.get(lang)
                self.fail('This operation should fail for language %s' % lang)
            except MstException:
                pass

class TestStringMerge(unittest.TestCase):
    
    def setUp(self):
        self.languages = ['en', 'fr']
        self.texts = {}
        for lang in self.languages:
            self.texts[lang] = build_test_text(lang)

    def testMergeSucceeds(self):
        strings = []
        for lang in self.languages:
            s = String('key', [ lang ] )
            s.add( lang, build_test_text(lang) )
            strings.append(s)
        merged = String('key', [])
        for s in strings:
            merged.merge(s)
        for lang in self.languages:
            text = build_test_text(lang)
            self.assertEqual(text, merged.get(lang) )

    def testMergeWithSameLanguagesFail(self):
        string1 = String('key', self.languages )
        string2 = String('key', [ self.languages[0] ] )
        try:
            string1.merge(string2)
        except MstException:
            pass
            
    def testMergeWithDifferentKeysFail(self):
        string1 = String('key_a', self.languages )
        string2 = String('key_b', self.languages )
        try:
            string1.merge(string2)
        except MstException:
            pass

