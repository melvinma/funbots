import os
from os.path import expanduser
import configparser

class FunbotsConfig :
    '''
    Retrieve configuration from configuration file.
    Configuration file is retrieved following this logic:
        look for system variable "FUNBOTS_CONFIGURATION_FILE",
            if existing, load the file using value specified by FUNBOTS_CONFIGURATION_FILE
            if not existing, use "~/funbots/funbots.init"
    '''

    class __OnlyOne:
        def __init__(self, arg):
            self.conf = arg
        def __str__(self):
            return repr(self) + self.conf

    ## static variable
    instance = None

    def __init__(self):
        if FunbotsConfig.instance is None:
            filePath=os.environ.get('FUNBOTS_CONFIGURATION_FILE')
            if filePath is None:
                home = expanduser("~")
                filePath = os.path.join(home, 'funbots/funbots.init')
            conf = configparser.ConfigParser()
            conf.read(filePath)
            ##print(conf.sections())
            FunbotsConfig.instance = FunbotsConfig.__OnlyOne(conf)

    def googleVisionKey(self) :
        return self.instance.conf['Google Vision']['gvkey']
