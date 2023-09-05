import os

from dotenv import load_dotenv
from interactions import MISSING

CONFIG_NAME = os.getenv('ENVIRONMENT') or 'default'
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.getcwd() + "/.env"
load_dotenv(dotenv_path=env_path)

class Config:
    DEBUG = False
    """
    The scope for the bot to operate in.
    This should be a guild ID or list of guild IDs
    """
    DEV_GUILD = os.environ.get('DEV_GUILD')

class DevelopmentConfig(Config):
    DEBUG = True

class StagingConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    DEV_GUILD = MISSING

configs = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}

config = configs[CONFIG_NAME]