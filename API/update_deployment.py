#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def create_scale_object(new_scale):
	spec = client.ExtensionsV1beta1ScaleSpec(replicas=new_scale)
	scale_object = client.ExtensionsV1beta1Scale(
					api_version = "extensions/v1beta1",
					spec = spec)

	return scale_object

def update_deployment_scale(scale_object, namespace, deployment_name):
    name = 'new_scale'
    pretty = 'True'
    try:
	    api_response = api_instance.replace_namespaced_deployment_scale(
	        name=name,
	        namespace=namespace,
	        body=scale_object,
	        pretty = pretty)
    except ApiException as e:
        print("Exception when calling Extension/v1beta->replace_namespaced_deployment_scale: %s \n" % e)
    return api_response
