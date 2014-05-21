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
import mst.gspread as gspread
from mst.exceptions import MstException


class Loader(object):
    '''
    Base loader class. All classes loading translation text data should
    derive from this one.
    '''
    def __init__(self):
        self.__data = []
        self.__loaded = False

    @property
    def data(self):
        return self.__data
    
    @property
    def rows(self):
        return len(self.__data)
    
    @data.setter
    def data(self, value):
        if self.__loaded == False:
            if isinstance(value, list):
                self.__data = value
                self.__loaded = True
            else:
                raise ValueError('Expected array of rows, but got %s instead' % value.__class__.__name__)
        else:
            raise RuntimeError('Data already loaded. Cannot overwrite.')


class LoaderCsv(Loader):
    '''
    This loader will load translation data from CSV file.
    '''
    def __init__(self, file):
            Loader.__init__(self)
            self.__file = file
            
            try:
                csv_file = open(file, 'r')
            except:
                raise MstException("Cannot open CSV file with resources: %s" % file)
            
            csv_reader = csv.reader(csv_file)
            rows = []
            for row in csv_reader:
                rows.append(row)
            self.data = rows
        
    def __str__(self):
        return 'CSV loader, file %s, rows: %s' % (self.__file, self.rows)

class LoaderGoogle(Loader):
    '''
    This loader reads data from Google Docs spreadsheet. You must provide
    emails and password for loggin-in and spreadsheet name. By default
    it will read worksheet named 'strings'.
    '''
    def __init__(self, user, password, spreadsheet, worksheet = 'strings'):
        Loader.__init__(self)
        self.__username = user
        self.__password = password
        self.__spreadsheet = spreadsheet
        self.__worksheet = worksheet
        self.__params = (self.username, self.password, self.spreadsheet, self.worksheet, self.rows)
        self.__load_data()
        
    def __str__(self):
        return 'Google Spreadsheet loader, username: %s, password: %s, spreadsheet %s.%s, rows: %s' % self.__params
        
    def __load_data(self):
        try:
            gc = gspread.login(self.username, self.password)
            spreadsheet = gc.open(self.spreadsheet)
            worksheet = spreadsheet.worksheet(self.worksheet)
            self.data = worksheet.get_all_values()
        except:
            raise MstException("Cannot load Google Spreadsheet: %s" % str(self.__params) )
    
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    @property
    def spreadsheet(self):
        return self.__spreadsheet

    @property
    def worksheet(self):
        return self.__worksheet