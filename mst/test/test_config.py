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
from mst.config import Config
from os import path

from mst.test.reference import AndroidConfig

class TestAndroidConfig(unittest.TestCase):
    
    def setUp(self):
        root = path.dirname( AndroidConfig.config_file_path )
        file = path.basename( AndroidConfig.config_file_path )
        self.config = Config(root, True, file)

    def testConfigGeneratorIsParsed(self):
        self.assertEqual(self.config.generator, AndroidConfig.generator_name )

    def testLanguagesAreProperlyExtracted(self):
        # we sort lists before comparison as the order is not important
        self.assertEqual( sorted(self.config.languages), sorted(AndroidConfig.languages) )
        
    def testPathsAreProperlyResolved(self):
        pass
#         for lang in AndroidConfig.languages:
#             output_path = self.config.output_file_path(lang)
#             self.assertEqual( output_path, AndroidConfig.paths[lang] )

