#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import yml
from kubernetes import client, config
import json

def delete_deployment(api_instance, deployment_name):
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=deployment_name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))