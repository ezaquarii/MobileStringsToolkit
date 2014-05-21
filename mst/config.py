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

import json
import os
from mst.exceptions import MstException

class Config(object):
    """
    Configuration parser - configuration is stored as JSON.
    """

    def __init__(self, project_root, verbose=False,  config_file='mst.cfg'):
        try:
            self.__root = os.path.abspath( project_root )
            self.__verbose = verbose
            file_path = os.path.join(self.root, config_file)
            file = open(file_path, 'r')
            data = json.load(file)
            self.__generator = data['generator']
            self.__paths = data['paths']
            self.__sorted = data.get('sorted', True)
        except FileNotFoundError:
            raise MstException("Cannot open config file: %s" % os.path.join(project_root, config_file) )
        
    def __str__(self):
        return "%s: languages: %s, generator: %s" % (type(self).__name__, self.languages, self.generator)
        
    @property
    def generator(self):
        """
        Resources generator type.
        """
        return self.__generator
    
    @property
    def languages(self):
        """
        List of languages we generate resources for.
        """
        keys = []
        for lang_code in self.__paths:
            keys.append( lang_code )
        return keys
    
    @property
    def verbose(self):
        """
        Verbose flag. If True, logs are written.
        """
        return self.__verbose
    
    @property
    def root(self):
        """
        Project root, where generated files will be written.
        """
        return self.__root

    @property
    def sorted(self):
        """If True, strings should be sorted by key"""
        return self.__sorted

    def resource_file_path(self, language):
        """
        Returns file path for a given language. File will be
        located in project root directory.
        """
        return os.path.join( self.root, self.__paths[language] )
