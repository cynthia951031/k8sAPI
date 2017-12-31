#__init__
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import kubernetes.client
from kubernetes import client

db = SQLAlchemy()

configuration = kubernetes.client.Configuration()
Configuration.api_key['authorization'] = config['KUBE_TOKEN']

api_instance = client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(configuration))

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	db.init_app(app)

	with app.app_context():
		db.create_all()

	return app

