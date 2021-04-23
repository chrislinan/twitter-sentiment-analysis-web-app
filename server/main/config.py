# project/server/config.py
import os

class BaseConfig:
    """Base configuration."""
    FLASK_APP="main/__init__.py"
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    CONSUMER_KEY = 'Dk9hL45i7ZYPCsrzoQQ8fHg9O'
    CONSUMER_SECRET = 'l3zhEQCowCcAR4mkEvQFRBaKUZGyVWKeIoZGK1RZ1e4B95MFoi'
    ACCESS_TOKEN = '817414278143770625-DaOy4OhVEzbLtunz9z03Fiwdsqjioa9'
    ACCESS_TOKEN_SECRET = 'C5OSm4FiYXNs6NbQGGtmQRFgIyxUEsZVvttTtUNJz3ziy'
    MONKEY_LEARN_SENTIMENT_TOKEN='63ea6d3ae42021fb16a1797ed1f85e8543494a51'
    MODEL_ID = 'cl_pi3C7JiL'
    KEY_WORDS_MODEL_ID = 'ex_YCya9nrn'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV="development"

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    FLASK_ENV="testing"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV="production"
