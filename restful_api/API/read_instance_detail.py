#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def read_instance_detail(namespace_name, instance_name):
	try:
		api_response = api_instance.read_namespaced_replication_controller(instance_name, namespace_name)
	except ApiException as e:
		print("Exception when calling CoreV1Api->read_namespaced_replication_controller: %s\n" % e)
	return api_response

def read_service_detail(namespace_name, instance_name):
	try: 
		api_response = api_instance.read_namespaced_service(instance_name, namespace_name)
	except ApiException as e:
		("Exception when calling CoreV1Api->read_namespaced_service: %s\n" % e)
	return api_response

'''
param		type
'''
'''
scale		int
cpu		  int
mem		  int
isSSD		  bool
creation_time  datatime
deletion_time  datatime
uid			str
'''
'''
return dict
'''
def parse_rc(api_response):
	rc_spec = api_response.spec
	pod_spec = rc_spec.template.spec
	scale = rc_spec.replicas
	resources = pod_spec.containers[0].resources
	cpu = resources.requests['cpu']
	mem = resources.requests['memory']
	isSSD_str = pod_spec.volumes[0].empty_dir
	if isSSD_str == 'memory':
		isSSD = False
	elif isSSD_str == 'SSD':
		isSSD = True
	meta = api_response.metadata
	create_time = meta.creation_timestamp 
	deletion_time = meta.deletion_timestamp 
	uid = meta.uid
	return dict(scale = scale, cpu = cpu, mem = mem, isSSD = isSSD, \
		creation_time = creation_time, deletion_time = deletion_time, uid = uid)

'''
param		type
'''
'''
ip           str
ports		 list(int)
'''

def parse_service(api_response):
	ip = api_response.spec.cluster_ip
	ports = api_response.spec.ports
	ports_list = [ each.port for each in ports ]

	return dict(ip = cluster_ip, ports = ports_list)


