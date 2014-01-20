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

import xml.dom.minidom as xml
import os

from mst.resources import (String, StringArray, QuantityStrings)

class Escape(object):
    @staticmethod
    def escape(string):
        '''
        Escape special characters. Remove escape characters before changing all
        chars to avoid accumulating slashes (\).
        @param  string: string to escape
        @return: string with characters escaped
        '''
        # FIX: use regexp here, it's a small hack to do my job today
        return string.replace("\\'", "\'").replace("\'", "\\'")

class GeneratorFactory(object):
    """
    Factory for generator objects. It can create generator
    for iOS or Android.
    """
    
    ANDROID = 'android'
    IOS = 'ios'
    
    @staticmethod
    def create(generator_type):
        if generator_type == GeneratorFactory.ANDROID:
            return AndroidGenerator()
        elif generator_type == GeneratorFactory.IOS:
            raise NotImplementedError('iOS generator is not implemented yet')
        else:
            raise RuntimeError('Unknown generator requested: ' + str(generator_type) )
        

class Generator(object):
    """
    Base class for all string resources generators. All generators
    should derive this class and implement abstract methods:
    
    * _addString()
    * _addStringArray()
    * _addQuantityString()
    """
    
    def __init__(self):
        pass
    
    def addResources(self, resources, language):
        """
        Add resources to the generator. It adds iterable collection
        of resource objects.
        """
        for res in resources:
            if isinstance(res, String):
                self._addString(res, language)
            elif isinstance(res, StringArray):
                self._addStringArray(res, language)
            elif isinstance(res, QuantityStrings):
                self._addQuantityString(res, language)
            else:
                raise TypeError("Unknown resource type: %s" % str( res.__class__) )
    
    def write(self, file):
        raise NotImplemented('Abstract method is not implemented')
    
    def _addString(self, resource, language):
        raise NotImplemented('Abstract method is not implemented')
    
    def _addStringArray(self, resource, language):
        raise NotImplemented('Abstract method is not implemented')
    
    def _addQuantityString(self, resource, language):
        raise NotImplemented('Abstract method is not implemented')


    
class AndroidGenerator(Generator):
    '''
    This is a string resources generator for Android platform. It will generate
    resource XML strings that you can write to your res/values files.
    
    By default it starts with empty DOM. Add resources to populate DOM and read
    XML string once you're done.
    '''
    def __init__(self):
        Generator.__init__(self)
        self.doc = xml.Document()
        self.root = self.doc.createElement('resources')
        self.doc.appendChild(self.root)
    
    def _addString(self, resource, language):
        string = self.doc.createElement('string')
        string.setAttribute('name', resource.key)
        text = Escape.escape(resource.get(language))
        text_node = self.doc.createTextNode( text )
        string.appendChild(text_node)
        self.root.appendChild(string)
        
    def _addStringArray(self, resource, language):
        array = self.doc.createElement('string-array')
        array.setAttribute('name', resource.key)
        for item_text in resource.get_array(language):
            text = Escape.escape( item_text )
            text_node = self.doc.createTextNode( text )
            item_element = self.doc.createElement('item')
            item_element.appendChild(text_node)
            array.appendChild(item_element)
        self.root.appendChild(array)

    def _addQuantityString(self, resource, language):
        plurals = self.doc.createElement('plurals')
        plurals.setAttribute('name', resource.key)
        # check for each quantity defined in schema and
        # add add it to XML only of string is not empty
        for quantity in QuantityStrings.QUANTITIES:
            quantity_string = Escape.escape( resource.get_quantity_string(language, quantity) )
            if len(quantity_string) > 0:
                text_node = self.doc.createTextNode(quantity_string)
                item_element = self.doc.createElement('item')
                item_element.setAttribute('quantity', quantity)
                item_element.appendChild(text_node)
                plurals.appendChild(item_element)
        self.root.appendChild(plurals)

    @property
    def xml(self):
        '''
        Create XML string from current DOM.
        '''
        return self.doc.toprettyxml()
    
    def write(self, file):
        # first ensure directory is created
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # open and write file contents
        f = open(file, 'w')
        f.write( self.xml )
        f.close()
        
        
    