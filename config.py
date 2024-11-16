import os 


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/test_01')
    SQLALCHEMY_TRACK_MODIFICATIONS = False