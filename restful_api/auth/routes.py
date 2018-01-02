#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from flask import Flask, jsonify
from flask import request, Response
from ..models import K8SUser, Instance
from .. import db
from . import auth

from ..API import create_namespace as create
@auth.route('/auth', methods=['POST', 'GET'])
def login():
	login_data = request.json
	name = login_data["name"]
	id = login_data["id"]
	user = User.query.filter_by(id = id).first()
	'''
	如果用户不存在新建用户以及 namespace
	用户 namespace 就是用户名
	'''
	if user is None:
		user = K8SUser(name = name, id = id, namespace = name)
		namespace_object = create_namespace_object(namespace_name = str(name))
		api_response = create_namespace(namespace_object)
		db.session.add(user)
		db.session.commit()

	token = user.get_token()
	response = make_response()
	response.set_cookie('kubernetes_token', value = token)

	return response