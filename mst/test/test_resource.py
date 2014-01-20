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
from mst.resources import Resource, ResourceText
from hashlib import md5
from os import urandom
from random import randint, shuffle

class TestResource(unittest.TestCase):

    MAX_KEYS = 255

    @property
    def random_keys(self):
        return self.__random_keys.copy()
    
    @property
    def keys_count(self):
        return len( self.__random_keys )

    @property
    def sorted_keys(self):
        return sorted( self.__random_keys )

    def get_randomized_resources(self):
        resources = []
        for key in self.random_keys:
            resources.append( Resource(key) )
        return resources

    def setUp(self):
        self.__random_keys = []
        generator = md5()
        total = randint(3, TestResource.MAX_KEYS)
        for i in range( total ):
            generator.update( urandom(1) )
            key = generator.hexdigest()
            self.__random_keys.append( key )
        self.assertGreater(total, 0)
        self.assertEqual(len(self.random_keys), total)
            

    def testSortingResourcesByKey(self):
        resources = self.get_randomized_resources()
        keys = self.sorted_keys
        self.assertEqual( len(resources), len(keys) )
        resources.sort()   
        for index in range( len(keys) ):
            self.assertEqual( keys[index], resources[index].key )
            
    def testSortingListContainingNonResourceObjectFailsWithTypeError(self):
        resources = self.get_randomized_resources()
        resources.append( object() )
        shuffle( resources )
        self.assertGreater( len(resources), 1 )
        self.assertEqual( len(resources), self.keys_count + 1 )
        try:
            sorted( resources )
            self.fail('Sorting Resource list containing alien object shall throw TypeError')
        except TypeError:
            pass
        

class TestResourceText(unittest.TestCase):
    
    def testOptionsAreEmptyByDefault(self):
        string = ResourceText('this is a string')
        self.assertTrue( isinstance( string.options, list ) )
        
    def testOptionsAreSetIfProvided(self):
        string = ResourceText('this is a string', ['1', '2', '3'] )
        self.assertEqual( string.options, ['1', '2', '3'] )
        
    def testOptionsAreImmutable(self):
        try:
            string = ResourceText('this is a string', ['1', '2', '3'] )
            string.options = []
            self.fail("Expected AttributeError exception")
        except AttributeError:
            pass
