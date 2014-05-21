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

from mst.exceptions import MstException
from mst import utils
import unicodedata

class ResourceText(str):
    """
    This is a standard string extended with additional options
    property. Options may be used by generators when generating
    output data from a given string.
    """
    
    def __new__(cls, text, options = []):
        s = str.__new__(cls, text)
        s.__options = options
        return s
    
    @property
    def options(self):
        return self.__options

class Resource(object):
    
    __key = None
    
    def __init__(self, key):
        self.key = key
    
    def __lt__(self, other):
        """
        Comparision of objects are used for sorting lists of resources.
        Sorting is done by resource keys.
        """
        if isinstance(other, Resource) == False:
            raise TypeError("Comparing %s object to something else: %s" (self.__class__, other.__class__) )
        return (self.key < other.key)
    
    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.key)
    
    @property
    def name(self):
        return self.__class__.__name__

    @property
    def key(self):
        return self.__key
    
    @key.setter
    def key(self, value):
        if self.key != None:
            raise AttributeError("This attribute can be assigned only one. It's current value is '%s'" % self.key)
        elif value.__class__ != "".__class__:
            raise ValueError("Expected key as string")
        else:
            self.__key = value

class String(Resource):
    '''
    This class represents standard string resource. It can contain multiple
    text translations.
    '''

    def __init__(self, key, languages):
        Resource.__init__(self, key)
        self.strings = {}
        for lang in languages:
            self.strings[lang] = ''
        
    @property
    def languages(self):
        return set( self.strings.keys() )
            
    def add(self, language, string):
        if language in self.strings:
            self.strings[ language ] = unicodedata.normalize('NFC', string)
        else:
            raise MstException("Can't add string. Requested language '%s' not existing" % language)
    
    def get(self, language):
        if language in self.strings:
            return self.strings[ language ]
        else:
            raise MstException("Can't get string. Requested language '%s' not existing" % language)
    
    def merge(self, string):
        if( self.key != string.key ):
            raise MstException('Trying to merge String resources with different keys: %s != %s', (self.key, string.key) )
        intersection = self.languages.intersection(string.languages)
        if( len( intersection ) > 0 ):
            raise MstException('Trying to merge Strings containing common languages: %s' % intersection )
        for lang in string.languages:
            self.languages.add(lang)
            self.strings[lang] = string.get(lang)
    
    def __str__(self):
        builder = []
        for lang in self.languages:
            text = utils.ellipsis( self.strings[lang] )
            builder.append( "'%s': '%s'" % (lang, text) )
        args = { 'class': self.__class__.__name__, 'langs': self.languages, 'strings': ', '.join(builder) }
        return "%(class)s: langs: %(langs)s, strings: {%(strings)s}" % args

    def __lt__(self, other):
        return self.key < other.key
        
        
class StringArray(Resource):
    '''
    String-array resource. It can keep multiple, ordered strings 
    '''
    
    def __init__(self, key, languages):
        Resource.__init__(self, key)
        self.__string_arrays = {}
        for lang in languages:
            self.string_arrays[lang] = {}
    
    @property
    def languages(self):
        return set(self.string_arrays.keys())
    
    @property
    def string_arrays(self):
        return self.__string_arrays
    
    def array(self, language):
        return self.string_arrays[language]
    
    def add(self, language, index, string):
        if not isinstance(language,str) or not isinstance(index, int) or not isinstance(string, str):
            raise TypeError('Wrong argument types: %s, %s, %s' % (type(language), type(index), type(string)) )
        if language in self.string_arrays:
            array = self.string_arrays[ language ]
            array[ int(index) ] = unicodedata.normalize('NFC', string) # fixme: index should be int
        else:
            raise MstException("Can't add string to array. Requested language '%s' not existing" % language)
    
    def get(self, language, index):
        if language in self.string_arrays:
            array = self.string_arrays[ language ]
            return array[index]
        else:
            raise MstException("Can't get string from array. Requested language '%s' not existing" % language)
        
    def get_array(self, language):
        if language in self.string_arrays:
            array = self.string_arrays[ language ]
        else:
            raise MstException("Can't get string from array. Requested language '%s' not existing" % language)
        items = []
        for index in sorted( array.keys() ):
            items.append( array[index] )
        return items
        
    def size(self, language):
        if language in self.string_arrays:
            array = self.string_arrays[ language ]
            return len( array )
        else:
            raise MstException("Can't get string array. Requested language '%s' not existing" % language)
   
    def merge(self, array):
        if( self.key != array.key ):
            raise MstException('Trying to merge %s resources with different keys: %s != %s', (self.name, self.key, array.key) )
        intersection = self.languages.intersection(array.languages)
        if( len( intersection ) > 0 ):
            raise MstException('Trying to merge %s containing common languages: %s' % (self.name, intersection) )
        
        for lang in array.languages:
            self.__string_arrays[lang] = array.array(lang)
            
        
    def __str__(self):
        args = { 'class': self.__class__.__name__, 'langs': self.languages }
        return "%(class)s: languages %(langs)s" % args
  
        
class QuantityStrings(Resource):
    '''
    '''
    
    ZERO  = "zero"
    ONE   = "one"
    TWO   = "two"
    FEW   = "few"
    MANY  = "many"
    OTHER = "other"
    
    QUANTITIES = [ ZERO, ONE, TWO, FEW, MANY, OTHER ]

    def __init__(self, key, languages):
        Resource.__init__(self, key)
        self.__quantity_strings = {}
        # quantity strings are empty for all languages by default
        for lang in languages:
            self.__quantity_strings[lang] = {}
            for quantity in QuantityStrings.QUANTITIES:
                self.__quantity_strings[lang][quantity] = ''
    
    def __validate_quantity(self, quantity):
        if quantity in QuantityStrings.QUANTITIES:
            pass
        else:
            raise ValueError("Invalid quantity '%s'. Accepted values are: %s" % (quantity, QuantityStrings.QUANTITIES) )
        
    def __str__(self):
        args = { 'class': self.__class__.__name__, 'langs': self.languages }
        return "%(class)s: languages %(langs)s" % args

    @property
    def languages(self):
        return set(self.__quantity_strings.keys())

    def get_quantities(self, language):
        return self.__quantity_strings[language]

    def add_quantity_string(self, language, quantity, string):
        self.__validate_quantity(quantity)
        if language in self.__quantity_strings:
            quantities = self.__quantity_strings[ language ]
            quantities[quantity] = unicodedata.normalize('NFC', string)
        else:
            raise MstException("Can't add string to quantities dictionary. Requested language '%s' not existing" % language)

    def get_quantity_string(self, language, quantity):
        if language in self.__quantity_strings:
            quantities = self.__quantity_strings[ language ]
            return quantities[quantity]
        else:
            raise MstException("Can't get string from quantities dictionary. Requested language '%s' not existing" % language)

    def merge(self, resource):
        if( self.key != resource.key ):
            raise MstException('Trying to merge %s resources with different keys: %s != %s', (self.name, self.key, resource.key) )
        intersection = self.languages.intersection(resource.languages)
        if( len( intersection ) > 0 ):
            raise MstException('Trying to merge %s containing common languages: %s' % (self.name, intersection) )
        
        for lang in resource.languages:
            for quantity in self.QUANTITIES:
                self.quantity_string[lang][quantity] = resource.get(lang, quantity)
    
