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
import unicodedata

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


class Generator(object):
    """
    Base class for all string resources generators. All generators
    should derive this class and implement abstract methods:
    
    * _addString()
    * _addStringArray()
    * _addQuantityString()
    """
    
    def __init__(self, sorted=False):
        self.__strings = []
        self.__arrays = []
        self.__plurals = []
        self.__sorted = sorted

    def init(self):
        raise NotImplementedError('Abstract method is not implemented')

    @property
    def sorted(self):
        return self.__sorted

    @sorted.setter
    def sorted(self, s):
        self.__sorted = s

    def add_resources(self, resources):
        """
        Add resources to the generator. It adds iterable collection
        of resource objects.
        """
        for res in resources:
            if isinstance(res, String):
                self.__strings.append(res)
            elif isinstance(res, StringArray):
                self.__arrays.append(res)
            elif isinstance(res, QuantityStrings):
                self.__plurals.append(res)
            else:
                raise TypeError("Unknown resource type: %s" % str( res.__class__) )

    def generate(self, language):
        self.init()
        strings = sorted(self.__strings) if self.sorted else self.__strings
        arrays = sorted(self.__arrays) if self.sorted else self.__arrays
        plurals = sorted(self.__plurals) if self.sorted else self.__plurals
        for s in strings:
            self._add_string(s, language)
        for a in arrays:
            self._add_string_array(a, language)
        for p in plurals:
            self._add_quantity_string(p, language)

    def write(self, file):
        raise NotImplementedError('Abstract method is not implemented')
    
    def _add_string(self, resource, language):
        raise NotImplementedError('Abstract method is not implemented')
    
    def _add_string_array(self, resource, language):
        raise NotImplementedError('Abstract method is not implemented')
    
    def _add_quantity_string(self, resource, language):
        raise NotImplementedError('Abstract method is not implemented')



class AndroidXmlGenerator(Generator):
    '''
    This is a string resources generator for Android platform. It will generate
    resource XML strings that you can write to your res/values files.
    
    By default it starts with empty DOM. Add resources to populate DOM and read
    XML string once you're done.
    '''
    def __init__(self):
        Generator.__init__(self)
        self.doc = None
        self.root = None

    def init(self):
        self.doc = xml.Document()
        self.root = self.doc.createElement('resources')
        self.doc.appendChild(self.root)
    
    def _add_string(self, resource, language):
        string = self.doc.createElement('string')
        string.setAttribute('name', resource.key)
        text = Escape.escape(resource.get(language))
        if len(text) > 0:
            text_node = self.doc.createTextNode( text )
            string.appendChild(text_node)
            self.root.appendChild(string)
        
    def _add_string_array(self, resource, language):
        array = self.doc.createElement('string-array')
        array.setAttribute('name', resource.key)
        for item_text in resource.get_array(language):
            if len(item_text) > 0:
                text = Escape.escape( item_text )
                text_node = self.doc.createTextNode( text )
                item_element = self.doc.createElement('item')
                item_element.appendChild(text_node)
                array.appendChild(item_element)
        self.root.appendChild(array)

    def _add_quantity_string(self, resource, language):
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


class AndroidGenerator(Generator):
    '''
    This is a string resources generator for Android platform. It will generate
    resource XML strings that you can write to your res/values files.

    By default it starts with empty DOM. Add resources to populate DOM and read
    XML string once you're done.
    '''
    def __init__(self):
        Generator.__init__(self)
        self.xml_head = '<?xml version="1.0" encoding="utf-8"?>\n<resources">\n\n'
        self.xml_tail = '\n\n</resources>'
        self.xml_body = ''

    def init(self):
        self.xml_body = ''

    def _add_string(self, resource, language):
        text = Escape.escape(resource.get(language))
        if len(text) > 0:
            string_item = '<string name="%s">%s</string>\n' % (resource.key, text)
            self.xml_body += string_item

    def _add_string_array(self, resource, language):
        xml_head = '<string-array name="%s">\n' % resource.key
        xml_tail = '</string-array>\n'
        xml_items = ''

        for item_text in resource.get_array(language):
            if len(item_text) > 0:
                xml_items += '\t<item>%s</item>\n' % Escape.escape(item_text)

        if len(xml_items) > 0:
            self.xml_body += xml_head + xml_items + xml_tail

    def _add_quantity_string(self, resource, language):
        xml_head = '<plurals name="%s">\n' % resource.key
        xml_tail = '</plurals>\n'
        xml_items = ''
        xml_item_fmt = '\t<item quantity="%s">%s</item>\n'
        # check for each quantity defined in schema and
        # add add it to XML only of string is not empty
        for quantity in QuantityStrings.QUANTITIES:
            quantity_text = Escape.escape( resource.get_quantity_string(language, quantity) )
            if len(quantity_text) > 0:
                xml_items += xml_item_fmt % (quantity, Escape.escape(quantity_text) )

        if len(xml_items) > 0:
            self.xml_body += xml_head + xml_items + xml_tail

    @property
    def xml(self):
        all = self.xml_head + self.xml_body + self.xml_tail
        return unicodedata.normalize('NFC', all)

    def write(self, file):
        # first ensure directory is created
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # open and write file contents
        f = open(file, 'w')
        f.write( self.xml )
        f.close()

        
class AppleGenerator(Generator):

    def __init__(self):
        Generator.__init__(self)
        self.doc = ''

    def init(self):
        self.doc = ''

    def _add_string(self, resource, language):
        text = resource.get(language)
        if len(text) > 0:
            self.doc += '"%s" = "%s";\n' % (resource.key, resource.get(language))

    def _add_string_array(self, resource, language):
        pass

    def _add_quantity_string(self, resource, language):
        pass

    def write(self, file):
        # first ensure directory is created
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # open and write file contents
        f = open(file, 'w')
        f.write( self.doc )
        f.close()
