import os


class DevelopmentConfig:
    # Flask
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
        **{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'hogehoge'),
            'host': os.getenv('DB_HOST', 'db'),
            'database': os.getenv('DB_DATABASE', 'matatabi')
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Swaggerのデフォルト表示形式をListにする
    SWAGGER_UI_DOC_EXPANSION = 'list'
    # Validationの有効化
    RESTPLUS_VALIDATE = True


Config = DevelopmentConfig
