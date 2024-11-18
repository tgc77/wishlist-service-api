from decouple import config


class APIConfig:
    CLIENTS_SERVICE_URL = config('CLIENTS_SERVICE_URL')
    CLIENTS_ROUTE_PREFIX = config('CLIENTS_ROUTE_PREFIX')
    PRODUCTS_SERVICE_URL = config('PRODUCTS_SERVICE_URL')
    PRODUCTS_ROUTE_PREFIX = config('PRODUCTS_ROUTE_PREFIX')
    FAVORITE_PRODUCTS_SERVICE_URL = config('FAVORITE_PRODUCTS_SERVICE_URL')
    FAVORITE_PRODUCTS_ROUTE_PREFIX = config('FAVORITE_PRODUCTS_ROUTE_PREFIX')
    RABBIT_PASSWORD = config('RABBIT_PASSWORD')
    RABBIT_USER = config('RABBIT_USER')
    RABBIT_HOST = config('RABBIT_HOST')
    RABBIT_PORT = config('RABBIT_PORT')
    MYSQL_RANDOM_ROOT_PASSWORD = config(
        'MYSQL_RANDOM_ROOT_PASSWORD', default=False)
    MYSQL_HOST = config('MYSQL_HOST')
    MYSQL_PORT = config('MYSQL_PORT')
    MYSQL_USERNAME = config('MYSQL_USERNAME')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD')
    MYSQL_DATABASE = config('MYSQL_DATABASE')
    DATABASE_CONNECTION_URI = config('DATABASE_CONNECTION_URI')
    SECRET_KEY = config('SECRET_KEY', cast=str)
    HASH_ALGORITHM = config('HASH_ALGORITHM', cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)
    API_GATEWAY_SERVICE_URL = config('API_GATEWAY_SERVICE_URL')