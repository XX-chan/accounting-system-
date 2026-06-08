import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = False
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR,"data","account.db")}"


class DevelopmentConfig(Config):

    DEBUG = True 
    
    SECRET_KEY = os.environ.get("SECRET_KEY","dev-default-key")

class ProductConfig(Config):

    DEBUG = False


config_by_name={
    "development":DevelopmentConfig,
    "product":ProductConfig,
    "default":DevelopmentConfig
}


#根据FLASK_CONFIG返回配置类
def get_config():
    name = os.environ.get("FLASK_CONFIG","default")
    return config_by_name(name,DevelopmentConfig)