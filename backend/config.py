class Config():

    SQLALCHEMY_DATABASE_URI = 'sqlite:///placement_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'THIS_IS_GOING_TO_BE_SECRET'
    

    JWT_SECRET_KEY = 'placement_portal_super_secret_key_123456789'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_ALGORITHM = 'HS256'
    

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'


    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/2'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'pp'
