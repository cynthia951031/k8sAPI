#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import yml
from kubernetes import client, config
import json

######################################

DEPLOYMENT_NAME = "nginx-deployment"


def create_deployment_object(scale, cpu, gpu, instancename, mem, isSSD):
    # Configureate Pod template container
    container = client.V1Container(
        name=instancename,
        image="nginx:1.7.9",
        resource=clinet.V1ResourceRequirements(requests={'cpu': str(cpu), 'memory':str(mem) + 'Mi'}),
        ports=[client.V1ContainerPort(container_port=80)])
    if isSSD:
        volume_medium = 'SSD'
    else:
        volume_medium = 'memory'
    volume = client.V1Volume(
        name='cache-volume',
        emptyDir=client.V1EmptyDirVolumeSource(medium=volume_medium))
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container], volumes =[volume]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=scale,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))




'''
def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    # Create a deployment object with client-python API. The deployment we
    # created is same as the `nginx-deployment.yaml` in the /examples folder.
    deployment = create_deployment_object()

    create_deployment(extensions_v1beta1, deployment)

    update_deployment(extensions_v1beta1, deployment)

    delete_deployment(extensions_v1beta1)'''
