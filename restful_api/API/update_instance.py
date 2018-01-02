#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def create_scale_object(new_scale):
	scale_spec = client.V1ScaleSpec(replicas = new_scale)
	status = client.V1ScaleStatus(replicas = new_scale)
	scale = client.V1Scale(api_version = 'corev1',
							kind = 'Scale',
							spec = scale_spec,
							status = status)
	return scale

def update_instance_scale(scale_object, instance_name, namespace_name):
	try: 
		api_response = api_instance.replace_namespaced_replication_controller_scale(name = instance_name, namespace = namespace_name, body = scale_object)
	except ApiException as e:
		print("Exception when calling CoreV1Api->replace_namespaced_replication_controller_scale: %s\n" % e)

	return api_response
