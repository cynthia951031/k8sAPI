#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_reponse, request, Response
from .API import create_deployment, delete_deployment, update_deployment

from . import models
from .models import K8SUser, Instance
from . import db
from flask import current_app
import jwt


API_URL = 'http://localhost:8080/'
BASE_URL = API_URL
KUBE_TOKEN = current_app.config['KUBE_TOKEN']


@app.route(BASE_URL + 'auth', methods=['POST'])
def login():
	'''print request''' 
	#不确定是不是 request.form
	login_data = request.form
	name = login_data["name"]
	id = login_data["id"]
	user = User.query.filter_by(id = id).first()
	#如果用户不存在新建用户以及 namespace
	if user is None:
		user = K8SUser(name = name, id = id, namespace = name)
		
		namespace_object = create_deployment_object(NAMESPACE_NAME = str(name))
		api_response = create_namespace(namespace_object)

		db.session.add(user)
		db.session.commit()

	token = user.get_token()
	response = make_response()
	response.set_cookie('kubernetes_token', value = token)

	return response

from .API.create_namespace import create_namespace, create_deployment_object
@app.route(BASE_URL + 'instance', methods=['POST'])
def create_instance():
	token = request.cookies
	user = K8SUser.validate_token(token)

	if user is not None:
		namespace = user.namespace
	else:
		return Response(status=400)

	'''print request''' 
	#不确定是不是 request.form
	data = request.form
	instance_name = data['instance']
	param = data['param']
	scale = param['scale']
	cpu = param['cpu']
	memory = param['memory']
	gpu = param['gpu']
	isSSD = param['isSSD']
	id = data['aid']

	deployment_object = create_deployment_object(scale=scale, 
										  cpu=cpu, 
										  gpu=gpu, 
										  instance_name=instance_name, 
										  mem=memory, 
										  isSSD=isSSD)

	api_response = create_deployment(deployment_object, namespace)


	new_ins = Instance(name=instance_name, id = id)
	db.session.add(new_ins)
	db.commit()
	
	return api_response

from .API.delete_deployment import delete_deployment
@app.route(BASE_URL + 'instance/<int::iid>', methods=['DELETE'])
def delete_instance(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)

	if user is not None:
		namespace = user.namespace
	else:
		return Response(status=400)

	ins = Instance.query.filter_by(id=iid).first()
	
	api_response = delete_deployment(str(ins.name), namespace)
	
	return api_response

from .API.update_deployment import update_deployment_scale, create_scale_object
@app.route(BASE_URL + 'instance/<int::iid>', methods=['PUT'])
def update_instance(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)

	if user is not None:
		namespace = user.namespace
	else:
		return Response(status=400)

	'''print request''' 
	#不确定数据的取出方式是不是 request.form
	data = request.form
	param = data['param']
	new_scale =  param['new_scale']

	ins = Instance.query.filter_by(id=iid).first()
	deployment_name = ins.name

	scale_object = create_scale_object(new_scale)
	api_response = update_deployment_scale(scale_object, namespace, str(ins.name))
	# todo:dealwith response
	return api_response

from .API.list_namespaced_deployment import list_namespaced_deployment
@app.route(BASE_URL + 'instance/query', methods=['GET'])
def query_instance():
	token = request.cookies
	user = K8SUser.validate_token(token)

	if user is not None:
		namespace = user.namespace
	else:
		return Response(status=400)
	'''print request''' 
	#不确定数据的取出方式是不是 request.form
	data = request.form

	kind = data['kind']

	api_response = list_namespaced_deployment(namespace_name=namespace)
	# todo: dealwith api_response
	return api_response

from .API.read_instance_detail import read_instance_detail
@app.route(BASE_URL + 'instance/<int::iid>', methods=['GET'])
def get_instance_detail(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)

	if user is not None:
		namespace = user.namespace
	else:
		return Response(status=400)

	ins = Instance.query.filter_by(id=iid).first()
	name = ins.name

	api_response = read_instance_detail(deployment_name=name, namespace_name=namespace)
	#return type: ExtensionsV1beta1Deployment
	return api_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


