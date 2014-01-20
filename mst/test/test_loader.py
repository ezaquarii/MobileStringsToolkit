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
import os
from mst.loader import LoaderCsv
from mst.loader import LoaderGoogle
from mst.test.reference import Spreadsheet as reference

class TestLoaderCsv(unittest.TestCase):

    def __reference_csv(self):
        directory = os.path.dirname(__file__)
        return os.path.join(directory, 'resources', 'ref.csv')

    def testLoader(self):
        loader = LoaderCsv( self.__reference_csv() )
        data = loader.data
        self.assertEquals( len(data), reference.total_rows, 'Expected to load data from file')

class TestLoaderGoogle(unittest.TestCase):
    
    # modify those to point to your own reference spreadsheet
    # load ref.csv into spreadsheet
    user        = 'user'
    password    = 'password'
    spreadsheet = 'mobile_string_tools_reference'
    worksheet   = 'strings'
    
    def testLoader(self):
        loader = LoaderGoogle(self.user, self.password, self.spreadsheet, self.worksheet)
        data = loader.data
        self.assertEqual( len( data ) , reference.total_rows, 'Expected to load data from spreadsheet')
        
