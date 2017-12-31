#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def list_namespaced_deployment(namespace_name):
	namespace = namespace_name
	pretty = 'True'

	try:
		api_response = api_instance.list_namespaced_deployment(namespace, pretty=pretty)
	except ApiException as e:
		print("Exception when calling Extension/v1beta->replace_namespaced_deployment_scale: %s \n" % e)
    return api_response