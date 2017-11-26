#__init__
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client, config

#config  kube
config.load_kube_config()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
db.init_app(app)


