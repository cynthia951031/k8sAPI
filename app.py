#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_reponse
from flask import request
from .API import create_deployment, delete_deployment, update_deployment

from . import models
from . import db
from .models import Instance

API_URL = 'http;//192.168.31.85:8080/'
BASE_URL = API_URL
NAMESPACE = 'default'

extensions_v1beta1 = client.ExtensionsV1beta1Api()



@app.route(BASE_URL + 'instance', methods=['POST'])
def create_instance():
	if not request.json or not 'instance_name' in request.json:
		abort(404)

	instance_name = request.json['instance_name']
	scale = request.json['scale']
	cpu = request.json['cpu']
	memory = request.json['memory']
	gpu = request.json['gpu']
	isSSD = request.json['isSSD']
	instance_id = request.json['aid']

	instance = models.param_to_model(instance_name=instance_name, 
									 instance_id=instance_id, 
									 cpu=cpu, 
									 gpu=gpu,
									 mem=memory,
									 scale=scale,
									 isSSD=isSSD)
	db.session.add(instance)
	db.session.commit()

	deployment = create_deployment_object(scale=scale, 
										  cpu=cpu, 
										  gpu=gpu, 
										  instance_name=instance_name, 
										  mem=memory, 
										  isSSD=isSSD)
	api_response = create_deployment(extensions_v1beta1, deployment)
	
	return {'status' : api_response.status}

@app.route(BASE_URL + 'instance/<int::iid>', methods=['DELETE'])
def delete_instance(iid):
	ins = Instance.query.filter_by(id=iid).first()
	
	api_response = delete_deployment(extensions_v1beta1, str(ins.name))
	
	return {'status' : api_response.status}

@app.route(BASE_URL + 'instance/<int::iid>', methods=['PUT'])
def update_instance(iid):
	if not request.json or not 'iid' in request.json:
		abort(404)
	new_scale = request.json['new_scale']

	ins = Instance.query.filter_by(id=iid).first()
	ins.scale = new_scale

	deployment = create_deployment_object(scale=new_scale,
										  cpu=ins.CPUsize,
										  gpu=ins.GPUnum,
										  instance_name=ins.name,
										  mem=ins.MEMsize,
										  isSSD=ins.isSSD)
	api_response = update_deployment(extensions_v1beta1, deployment, str(ins.name))
	
	if api_response.status == 200:
		db.session.commit()
	
	return {'status' : api_response.status}

@app.route(BASE_URL + 'instance/query', methods=['GET'])
def query_instance():
	if not request.json or not 'iid' in request.json:
		abort(404)

	iid = request.json['iid']
	ins = Instance.query.filter_by(id=iid).first()

	api_response = extensions_v1beta1.read_namespaced_deployment(name=ins.name, namespace=NAMESPACE)
	# transform api_response
	return

@app.route(BASE_URL + 'instance/<int::iid>', methods=['GET'])
def get_instance_detail(iid):
	ins = Instance.query.filter_by(id=iid).first()

	api_response = extensions_v1beta1.read_namespaced_deployment(name=ins.name, namespace=NAMESPACE)
	#transform api_response
	return

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

