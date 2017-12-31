#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def read_instance_detail(namespace_name, deployment_name):
	pretty = 'true'
	try:
		api_response = api_instance.read_namespaced_deployment(deployment_name, namespace, pretty=pretty)
	except ApiException as e:
        print("Exception when calling Extension/v1beta->replace_namespaced_deployment_scale: %s \n" % e)
    return api_response