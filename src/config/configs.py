from configparser import ConfigParser

conf_obj = ConfigParser()
conf_obj.read('src/config/conf.ini')

try:
    conf = conf_obj['DATABASE']
    SERVER = conf.get('server')
    DATABASE = conf.get('database')
    DRIVER = conf.get('driver')
except:
    pass
