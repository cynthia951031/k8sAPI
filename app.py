#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_reponse
from flask import request

app = Flask(__name__)

API_URL = 'http;//192.168.31.85:8080/'
BASE_URL = API_URL

@app.route(BASE_URL + 'instance', methods=['POST'])
def create_instance():
	if not request.json or not 'instancename' in request.json:
		abort(404)

	instancename = request.json['instancename']
	nodes = request.json['nodes']
	cpu = request.json['cpu']
	memory = request.json['memory']
	gpu = request.json['gpu']
	isSSD = request.json['isSSD']

	return

@app.route(BASE_URL + 'instance/<int::iid>', methods=['DELETE'])
def delete_instance(iid):

	return

@app.route(BASE_URL + 'instance/<int::iid>', methods=['PUT'])
def update_instance(iid):
	if not request.json or not 'iid' in request.json:
		abort(404)
	new_scale = request.json['new_scale']
	return

@app.route(BASE_URL + 'instance/query', methods=['GET'])
def query_instance():
	if not request.json or not 'iid' in request.json
	return

@app.route(BASE_URL + 'instance/<int::iid>', methods=['GET'])
def get_instance_detail(iid):
	return

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

