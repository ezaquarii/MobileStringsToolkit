__author__ = 'nomtek'

from mst import loader
from mst import generator
from mst.exceptions import MstException

class Factory(object):

    LOADER_GOOGLEDOCS = 'googledocs'
    LOADER_CSV = 'csv'

    @staticmethod
    def create_loader(loader_type, loader_args):
        if loader_type == Factory.LOADER_GOOGLEDOCS:
            user = loader_args[0]
            password = loader_args[1]
            spreadsheet = loader_args[2]
            return loader.LoaderGoogle(user, password, spreadsheet)
        elif loader_type == Factory.LOADER_CSV:
            file = loader_args[0]
            return loader.LoaderCsv(file)
        else:
            msg = 'Unknown loader requested: %s. Allowed: %s' % ( str(loader_type), [Factory.LOADER_CSV, Factory.LOADER_GOOGLEDOCS])
            raise RuntimeError(msg)

    GENERATOR_ANDROID = 'android'
    GENERATOR_ANDROID_XML = 'android_xml'
    GENERATOR_IOS = 'ios'

    @staticmethod
    def create_generator(generator_type):
        d = {
            Factory.GENERATOR_ANDROID: generator.AndroidGenerator,
            Factory.GENERATOR_ANDROID_XML: generator.AndroidXmlGenerator,
            Factory.GENERATOR_IOS:     generator.AppleGenerator
        }
        try:
            return d[generator_type]() # get type and call object constructor
        except KeyError:
            msg = "Unknown generator requested: %s. Allowed: %s" % (str(generator_type), sorted(list(d.keys())))
            raise MstException(msg)

    @staticmethod
    def create_key_id(generator_type):
        d = {
            Factory.GENERATOR_ANDROID: "android_id",
            Factory.GENERATOR_ANDROID_XML: "android_id",
            Factory.GENERATOR_IOS: "ios_id"
        }
        try:
            return d[generator_type]
        except KeyError:
            msg = "Unknown generator requested: %s. I don't know how to choose key. Allowed: %s" % (str(generator_type), sorted(list(d.keys())))
            raise MstException(msg)