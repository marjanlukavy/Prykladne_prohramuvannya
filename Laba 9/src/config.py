import os
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())

class Development(object):

    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class Testing(object):

    TESTING = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://marjanlukavyi:popqasef@localhost:5432/blog_api_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
