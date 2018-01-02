#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import request, Response
from ..models import K8SUser, Instance
from .. import db
from . import instance
import datetime



from ..API import create_namespaced_instance as create
@instance.route('/', methods=['POST'])
def create_instance():
	token = request.cookies
	user = K8SUser.validate_token(token)
	if user is not None:
		namespace = user.namespace
	else:
		return jsonify(dict(message = "you may not login in ")), 400

	data = request.json
	instance_name = data['instance']
	param = data['param']
	scale = param['scale']
	cpu = param['cpu']
	memory = param['memory']
	gpu = param['gpu']
	isSSD = param['isSSD']
	id = data['aid']
	'''
	one replication controller corresponse to one service
	'''
	rc_object = create.create_rc_object(scale = scale, cpu = cpu, gpu = gpu, instance_name = instance_name, mem = mem, isSSD = isSSD)
	rc_response = create.create_rc(namespace_name = namespace, rc_object = rc_object)
	service_object = create.create_service_object(instance_name = instance_name)
	service_response = create.create_namespaced_service(service_object = service_object, namespace_name = namespace)

	if rc_response is not None and service_response is not None:
		new_ins = Instance(name = instance_name, id = id, namespace = namespace)
		db.session.add(new_ins)
		db.commit()
		return jsonify(dict(message = 'both rc and service created')), 200
	else: # todo: can add more message
		return jsonify(dict(message = 'created failure')), 400

'''
return status == 'Success' or 'Failure'
complete!
'''
from ..API import delete_instance as delete
@instance.route('/<int:iid>', methods=['DELETE'])
def delete_instance(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)
	if user is not None:
		namespace = user.namespace
	else:
		return jsonify(dict(message = "you may not login in ")), 400

	ins = Instance.query.filter_by(id=iid).first()
	name = ins.name
	rc_response = delete.delete_instance(namespace_name = namespace, instance_name = name)
	service_response = delete.delete_service(namespace_name = namespace, instance_name = name)

	if rc_response.status == 'Success' and service_response.status == 'Success':
		ins.is_deleted = True
		db.session.add(ins)
		db.commit()
		return jsonify(dict(message = 'both rc and service deleted')), 200
	else: # todo: can add more message
		return jsonify(dict(message = 'deleted failure')), 400

'''
return status == 'Success' or 'Failure'
complete!
'''
from ..API import update_instance as update
@instance.route('/<int:iid>', methods=['PUT'])
def update_instance(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)
	if user is not None:
		namespace = user.namespace
	else:
		return jsonify(dict(message = "you may not login in ")), 400

	data = request.json
	param = data['param']
	new_scale =  param['new_scale']

	ins = Instance.query.filter_by(id=iid).first()
	name = ins.name

	scale_object = update.create_scale_object(new_scale)
	api_response = update.update_instance_scale(scale_object = scale_object, namespace_name = namespace, instance_name = name)
	
	if api_response is not None:
		ins.update_time = datetime.datetime.now()
		db.session.add(ins)
		db.commit()
		return jsonify(dict(message = 'scale updated')), 200
	else: # todo: can add more message
		return jsonify(dict(message = 'updated failure')), 400

'''
return json
see more about the data format in API/read_instande_detail.py
complete!
'''
from ..API import read_instance_detail as read
@instance.route('/<int:iid>', methods=['GET'])
def get_instance_detail(iid):
	token = request.cookies
	user = K8SUser.validate_token(token)
	if user is not None:
		namespace = user.namespace
	else:
		return jsonify(dict(message = "you may not login in ")), 400

	ins = Instance.query.filter_by(id=iid).first()
	name = ins.name
	instance_response = read.read_instance_detail(instance_name=name, namespace_name=namespace)
	service_response = read.read_service_detail(instance_name = name, namespace_name = namespace)

	instance_dict = read.parse_rc(instance_response)
	service_dict = read.parse_service(service_response)
	response = dict(name = ins.name, id = ins.id, update_time = ins.update_time).copy()
	response.update(instance_dict)
	response.update(service_dict)

	return jsonify(response), 200

@instance.route('query/', methods=['GET'])
def list_instance():
	token = request.cookies
	user = K8SUser.validate_token(token)
	if user is not None:
		namespace = user.namespace
	else:
		return jsonify(dict(message = "you may not login in ")), 400

	#检查 data 是否是 all 但实际上没什么用 leave it alone
	data = request.json

	ins_query = Instance.query.filter_by(namespace = namespace).all()
	ins_list = [dict(name = each.name, id = each.id, is_deleted = each.is_deleted, update_time = each.update_time) \
				for each in ins_query]

	return jsonify(dict(ins_list = ins_list)), 200












