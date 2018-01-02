#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from kubernetes import client
import json
from . import configuration, api_instance
from kubernetes.client.rest import ApiException


#不知道 gpu 在哪里
def create_deployment_object(scale, cpu, gpu, instance_name, mem, isSSD):
    container = client.V1Container(name = instance_name,
                                    resource = client.V1ResourceRequirements(requests = \
                                                                    dict(cpu = cpu, memory = mem)))
    if isSSD:
        volume_medium = 'SSD'
    else:
        volume_medium = 'memory'

    volume = client.V1Volume(name = instance_name,
                            emptyDir = client.V1EmptyDirVolumeSource(medium=volume_medium))
    template = client.V1PodTemplateSpec(spec = client.V1PodSpec(containers=[container], volumes =[volume]))
    spec = client.ExtensionsV1beta1DeploymentSpec(replicas=scale, 
                                                template=template)
    deployment = client.ExtensionsV1beta1Deployment(api_version="extensions/v1beta1",
                                                    kind="Deployment",
                                                    spec=spec)

    return deployment

def create_deployment(deployment_object, namespace_name):
    try:
        api_response = api_instance.create_namespaced_deployment(
            body=deployment_object,
            namespace=namespace_name)
    except ApiException as e:
        print("Exception when calling Extension/v1beta->create_namespaced_deployment: %s \n" % e)
    return api_response

