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

import argparse
from mst import Config
from mst import Factory
from mst import Spreadsheet
from mst import Log
from mst.exceptions import MstException

print("Mobile String Toolkit generator, v1.0\nCopyright (C) 2013 by Krzysztof Narkiewicz <krzysztof.narkiewicz@ezaquarii.com>\n")

try:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-r', '--project-root', required=True, nargs=1, help='Path to project root directory')
    parser.add_argument('-C', '--csv-loader', nargs=1, metavar='FILE', help='Load data from CSV file')
    parser.add_argument('-G', '--google-loader', nargs=4, metavar=('EMAIL', 'PASSWORD', 'SPREADSHEET', 'WORKSHEET'), help='Load data from Google Docs spreadsheet')
    parser.add_argument('-c', '--config', nargs=1, default=['mst.cfg'], help='Configuration file')
    parser.add_argument('-v',  '--verbose',  action='store_true',  help='Verbose mode')
    args = parser.parse_args()

    # load configuration from project root
    config = Config( args.project_root[0],  args.verbose, args.config[0] )
    Log.init(args.verbose)
    
    # create loader - this will also load resources data
    if args.csv_loader == None and args.google_loader != None:
        loader = Factory.create_loader( Factory.LOADER_GOOGLEDOCS, args.google_loader )
    elif args.csv_loader != None and args.google_loader == None:
        loader = Factory.create_loader( Factory.LOADER_CSV, args.csv_loader )
    else:
        raise MstException("""No loader defined in command line. I don't know how to load translations. RTF(riendly)M.""")

    key_id = Factory.create_key_id(config.generator)

    # create a spreadsheet with loaded data
    sheet = Spreadsheet(key_id, loader.data, config.languages)
    
    # extract resources from the spreadsheet
    strings = sheet.get_strings()
    string_arrays = sheet.get_string_arrays()
    quantity_strings = sheet.get_quantity_strings()
    
    Log.print( 'Project root:  %s' % config.root )
    Log.print( 'Generator:     %s' % config.generator )
    Log.print( 'Loader:        %s' % loader )
    Log.print( 'Languages:     %s' % ', '.join(config.languages) )
    Log.print( 'ID key:        %s' % key_id)
    Log.print( 'Sorted by key: %s' % config.sorted)
    Log.print( 'Generating language resources...' )

    generator = Factory.create_generator(config.generator)
    generator.sorted = config.sorted
    generator.add_resources(strings)
    generator.add_resources(string_arrays)
    generator.add_resources(quantity_strings)

    # for each language create a platform-specific generator and
    # generate resource files
    for language in config.languages:
        generator.generate(language)
        generator.write( config.resource_file_path(language) )
        if config.verbose:
            params = (language, config.resource_file_path(language), len(strings), len(string_arrays), len(quantity_strings) )
            Log.print(' * Language %s, file: %s, %s strings, %s arrays, %s plurals' % params)

# Very generic error handling
except MstException as e:
    print("ERROR: %s" % e)
    exit(1)
