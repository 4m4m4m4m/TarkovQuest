import os

class Config:
    SECRET_KEY = "dev-key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database1.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False