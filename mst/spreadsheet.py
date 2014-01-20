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

import csv
from mst.exceptions import MstException
from mst.resources import ResourceText, String, StringArray, QuantityStrings

class Spreadsheet(object):
    '''
    This class contains spreadsheet data. Spreadsheet is divided for two parts.
        - header section
        - data section
    It is able to parse the spreadsheet and extract all resources from it:
        - String
        - StringArray
        - QuantityStrings
    
    Header section contains type, IDs and languages. Type column contains
    type of string resource:
        - string - normal string
        - string-array - array of strings
        - plurals
    IDs columns contains proper string ID for each platform.
    Language columns contain language code correspoding to each string translation.
    
    Data section contains resources data.
    '''
    
    TYPE = 'type'
    OPTIONS = 'options'
    TYPE_STRING = 'string'
    TYPE_STRING_ARRAY = 'string-array'
    TYPE_QUANTITY_STRING = 'plurals'
    
    __resource_column_name = ''
    __header = []
    __data = []
    __languages = []
    
    __type_column = -1
    __id_column   = -1
    __language_column = {}
    __options_column = -1
    
    def __init__(self, resource_column, data, languages):
        """
        Initialize Spreadsheet object.
        resource column -- name of column with resource IDs, for ex. 'android_id'
        data -- data to be loaded (2D array of strings) or a path to CSV file
        languages -- array of language codes
        """
        self.__resource_column_name = resource_column
        self.__languages = languages
        
        if( type(data) == str ):
            self.__load_csv(data)
        elif( type(data) == list ):
            self.__load_data(data)
        else:
            raise TypeError("We can parse only 2-dimensional arrays of string data or load CSV files")
        
        self.__parse_data()
    
    def __str__(self):
        return "%s: header: %s, data: %s rows, languages: %s" % (self.__class__.__name__, self.header, len(self.data), self.languages)
    
    def __getitem__(self,index):
        '''Get data row'''
        return self.data[index]
        
    def __load_csv(self, file):
        '''Load data from CSV file'''
        data = []
        file = open(file, 'r')
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
        self.__load_data(data)
        
    def __load_data(self, data):
        '''Split data array for header and data'''
        self.__header = data[0]
        self.__data = data[1:]
        
    def __parse_data(self):
        """
        Parse data header and extract columns indexes for type, id and languages.
        """
        # find index of type column
        if self.TYPE in self.header:
            self.__type_column = self.header.index( self.TYPE )
        else:
            raise MstException("Can't fine %s column in header: %s" % (self.TYPE, self.header) )
        
        # find index of resource id column
        if self.__resource_column_name in self.header:
            self.__id_column = self.header.index( self.__resource_column_name )
        else:
            raise MstException("Can't find %s column in header: %s" % (self.__resource_column_name, self.header) )
        
        # find indexes of all language columns
        for language in self.__languages:
            if language in self.header:
                col = self.header.index( language )
                self.__language_column[language] = col
            else:
                raise MstException("Can't find %s column in header: %s" % (language, self.header) )
            
        # find index of options column
        if Spreadsheet.OPTIONS in self.header:
            self.__options_column = self.header.index( Spreadsheet.OPTIONS )
        else:
            raise MstException("Can't find %s column in header: %s" % (Spreadsheet.OPTIONS, self.header) )
   
    def _get_row_type(self, row):
        """"Extract type data of a given row"""
        return row[ self.type_column ]
    
    def _get_row_id(self, row):
        """Extract id from a given row"""
        return row[ self.id_column ]
    
    def _get_row_string(self, lang, row):
        """Extract string from a given row and language"""
        col = self.language_column[lang]
        return row[ col ]
    
    def _get_row_options(self, row):
        """
        Extract row options. Options are returned as a list of strings.
        If options is not available it returns empty list.
        """
        if self.options_column >= 0:
            opts = row[ self.options_column ]
            return opts.replace(' ', '').split(';')
        else:
            return [];
        
    def _has_valid_key(self, row):
        """
        Validate resource key.
        """
        #FIX: more checks here
        return len( row[ self.id_column ] ) > 0;
    
    def __get_string(self, row):
        """
        Get string resource from a given row. It loads resource
        object with translations for all languages and returns
        complete String instance.
        """
        key = row[ self.id_column ]
        resource = String(key, self.languages);
        for lang in self.languages:
            col = self.language_column(lang)
            text = row[ col ]
            options = self._get_row_options(row)
            resource.add(lang, ResourceText(text, options) )
        return resource

    @property
    def type_column(self):
        """Type column index"""
        return self.__type_column
    
    @property
    def id_column(self):
        """Resource ID column index""" 
        return self.__id_column
    
    def language_column(self, language):
        """Language column index for a given language"""
        return self.__language_column[language]

    @property
    def options_column(self):
        """Options column index"""
        return self.__options_column

    @property
    def header(self):
        """Entire header row stored as list of strings"""
        return self.__header

    @property
    def data(self):
        """Entire data section of the spreadsheet"""
        return self.__data

    @property
    def languages(self):
        """List of languages"""
        return self.__languages

    def get_strings(self):
        """Collect all String resources and return a list"""
        resources = []
        for row in self.data:
            if( self._get_row_type(row) == self.TYPE_STRING and self._has_valid_key(row) ):
                resource = self.__get_string(row)
                resources.append(resource)
        return resources
    
    def get_string_arrays(self):
        """Collect all StringArray resources and return a list"""
        resources = {}
        for row in self.data:
            if( self._get_row_type(row) == self.TYPE_STRING_ARRAY and self._has_valid_key(row) ):
                key_with_index = row[ self.id_column ]
                key, index = key_with_index.split(':')
                if (key in resources) == False:
                    resources[key] = StringArray(key, self.languages);
                sa = resources[key]
                for lang in self.languages:
                    col = self.language_column( lang )
                    text = row[ col ]
                    options = self._get_row_options(row)
                    sa.add(lang, int(index), ResourceText(text, options) ) #fixme: conversion not necessary
        return list( resources.values() )
        

    def get_quantity_strings(self):
        """Collect all QuantityStrings resources and return a list"""
        resources = {}
        for row in self.data:
            if( self._get_row_type(row) == self.TYPE_QUANTITY_STRING and self._has_valid_key(row) ):
                key_with_quantity = row[ self.id_column ]
                key, quantity = key_with_quantity.split(':')
                if (key in resources) == False:
                    resources[key] = QuantityStrings(key, self.languages);
                qs = resources[key]
                for lang in self.languages:
                    col = self.language_column( lang )
                    text = row[ col ]
                    options = self._get_row_options(row)
                    qs.add_quantity_string(lang, quantity, ResourceText(text, options) )
        return sorted( resources.values() )
    
    def get_all_resources(self):
        resources = []
        resources.extend( self.get_strings() )
        resources.extend( self.get_string_arrays() )
        resources.extend( self.get_quantity_strings() )
        return resources

        