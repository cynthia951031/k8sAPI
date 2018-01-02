#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def delete_rc(namespace_name, instance_name):
	options = client.V1DeleteOptions(api_version = 'corev1', 
										kind = "ReplicationController")
	try: 
		rc_api_response = api_instance.delete_namespaced_replication_controller(name = instance_name, namespace = namespace_name, body = options)
	except ApiException as e:
		print("Exception when calling CoreV1Api->delete_namespaced_replication_controller: %s\n" % e)

	return api_response

def delete_service(namespace_name, instance_name):
	try: 
		service_api_response = api_instance.delete_namespaced_service(name = instance_name, namespace = namespace_name)
	except ApiException as e:
		print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)

	return api_response