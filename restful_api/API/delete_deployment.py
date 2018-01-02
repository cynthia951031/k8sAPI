#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from kubernetes import client
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def delete_deployment(deployment_name, namespace_name):
    # Delete deployment
    body = client.V1DeleteOptions(api_version="extensions/v1beta1", 
    							kind = 'Deployment')
    try:
	    api_response = api_instance.delete_namespaced_deployment(
	        name=deployment_name,
	        namespace=namespace_name,
	        body=body)
    except ApiException as e:
        print("Exception when calling Extension/v1beta->delete_namespaced_deployment: %s \n" % e)
    return api_response