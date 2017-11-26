#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import yml
from kubernetes import client, config
import json

def update_deployment(api_instance, deployment, deployment_name):
    # Update container image
    #deployment.spec.replicas = new_scale
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=deployment_name,
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))
