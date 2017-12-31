#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Config:
	SECRET_KEY = 't0p s3cr3t'
    API_VERSION = 'extensions/v1beta1'

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'
	KUBE_TOKEN = 'KUBE_TOKEN...FILL_IT_LATER...'

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
