import os
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    MAX_CONTENT_LENGTH = 1*1024*1024
    
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        URI_VARS = ["DB_USER", "DB_PASS", "DB_NAME", "DB_DOMAIN"]
        uri_dict = {item: os.environ.get(item) for item in URI_VARS}
        for key in URI_VARS:
            if uri_dict[key] is None:
                raise ValueError(f"{key} is not set.")
        return f"postgresql+psycopg2://{uri_dict['DB_USER']}:{uri_dict['DB_PASS']}@{uri_dict['DB_DOMAIN']}/{uri_dict['DB_NAME']}"

    @property
    def AWS_ACCESS_KEY_ID(self):
        value = os.environ.get("AWS_ACCESS_KEY_ID")
        if not value:
            raise ValueError("AWS_ACCESS_KEY_ID is not set")
        return value

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        value = os.environ.get("AWS_SECRET_ACCESS_KEY")
        if not value:
            raise ValueError("AWS_SECRET_ACCESS_KEY is not set")
        return value

    @property
    def AWS_S3_BUCKET(self):
        value = os.environ.get("AWS_S3_BUCKET")
        if not value:
            raise ValueError("AWS_S3_BUCKET is not set")
        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
environment = os.environ.get("FLASK_ENV")
if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()