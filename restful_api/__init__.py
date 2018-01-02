#__init__
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	db.init_app(app)

	with app.app_context():
		db.create_all()

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/user')

	from .instance import instance as instance_blueprint
	app.register_blueprint(instance_blueprint, url_prefix='/instance')

	return app

