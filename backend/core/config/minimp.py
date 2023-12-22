from . import config

mpConfig = config['minimp'] if 'minimp' in config else {}

APPID = mpConfig['APPID']
SECRET =  mpConfig['SECRET']