class Config_ApiKeys(object):
    # configuration for encryption of api keys
    API_KEYS_DIR = './config/keys/'# should be with trailing slash
    API_KEYS_FILE_EXTENSION = '.key'
    API_KEYS_ENV=True # read from environment instead of key file
    API_KEYS=True 
