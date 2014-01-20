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

"""
This file describes reference data used for tests.
File must be updated each time we update reference data files.

Reference data base on reference CSV file with test data.

Each reference class should be imported as 'reference', to avoid
problems with code refactoring, for example:

``from mst.test.reference import Spreadsheet as reference``

@author: tn
"""

from os import path

def resource_file(*args):
    return path.join( path.dirname( path.realpath(__file__) ), 'resources', *args )

class Spreadsheet:
    """
    This class encapsulates reference data used for Spreadsheet tests
    """
    csv_file = resource_file( 'ref.csv' )
    
    type_column = 0
    id_column = 1
    languages = ['en', 'fr', 'es']
    language_columns = { 'en': 2, 'fr': 3, 'es': 4 }
    
    string_count = { 'en': 5, 'fr': 4, "es": 4 }
    string_rows = 5
    string_options = ['option1', 'option2', 'option3' ]
    string_resources = string_rows
        
    string_array_count = { 'en': 2, 'fr': 2, "es": 2 }
    string_array_rows = 2*4
    string_array_options = [ 'option_0', 'option_1', 'option_2', 'option_3' ]
    string_array_resources = 2
    
    quantity_strings_count = { 'en': 2, 'fr': 2, "es": 2 }
    quantity_strings_rows = 2*6
    quantity_strings_options = [ 'option_zero', 'option_one', 'option_two', 'option_few', 'option_many', 'option_other' ]
    quantity_strings_resources = 2
    
    total_rows = 31
    total_resources = ( string_resources + string_array_resources + quantity_strings_resources )
    
class AndroidConfig:
    config_file_path = resource_file('ref_android.cfg')
    generator_name = 'android'
    languages = ['en', 'es', 'fr']
    paths = {
                "en": "res/values/strings.xml",
                "fr": "res/values-fr/strings.xml",
                "es": "res/values-es/strings.xml"
            }
    paths_count = len( paths.keys() )
    languages_cound = len(languages)
    
class AndroidImporter(Spreadsheet, AndroidConfig):
    """
    This file describes project pseudo-environment. It is used in tests
    of XML importer. Data files and configuration file have to exist.
    """

    project_root_path = resource_file('')

    @staticmethod
    def xml_path(language):
        return resource_file( AndroidImporter.paths[language] )

