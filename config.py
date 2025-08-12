import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lms-secret-key-2025'
    
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    DB_NAME = os.environ.get('DB_NAME') or 'lms'
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    
    SESSION_TIMEOUT = 3600
    ITEMS_PER_PAGE = 10
    MAX_LOGIN_ATTEMPTS = 5
    
    @staticmethod
    def get_db_config():
        return {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME,
            'port': Config.DB_PORT,
            'autocommit': True
        }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
