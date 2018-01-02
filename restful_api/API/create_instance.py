#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from kubernetes import client
import json
from . import configuration, api_instance
from kubernetes.client.rest import ApiException

def create_service_object(instance_name):
	spec = client.V1ServiceSpec(
					selector = dict(name = instance_name))
	metadata = client.V1ObjectMeta(name = instance_name)
	service = client.V1Service(
					api_version = "corev1",
					kind = "Service", 
					spec = spec,
					metadata = metadata)

	return service

def create_namespaced_service(service_object, namespace_name):
	try:
		api_response = api_instance.create_namespaced_service(namespace_name, service_object)
	except ApiException as e:
		print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)


def create_rc_object(scale, cpu, gpu, instance_name, mem, isSSD):
	resources = client.V1ResourceRequirements(requests = dict(cpu = cpu, memory = mem))
	containers = client.V1Container(name = instance_name, resources = resources)
	if isSSD:
		medium = 'memory'
	else:
		medium = 'SSD'

	empty_dir = client.V1EmptyDirVolumeSource(medium = medium, size_limit = mem)
	volumes = client.V1Volume(name = instance_name, empty_dir = empty_dir)
	pod_spec = client.V1PodSpec(containers = [containers], volumes = [volumes])
	template = client.V1PodTemplateSpec(spec = spec)
	rc_spec = client.V1ReplicationControllerSpec(selector = dict(name, instance_name), 
											replicas = scale, 
											template = template)
	metadata = client.V1ObjectMeta(labels = dict(name, instance_name),
									name = instance_name)
	rc = client.V1ReplicationController(api_version = 'corev1', 
										kind = 'ReplicationController', 
										spec = rc_spec, 
										metadata = metadata)
	return rc

def create_rc(namespace_name, rc_object):
	try:
		api_response = api_instance.create_namespaced_replication_controller(namespace_name, rc_object)
	except ApiException as e:
		print("Exception when calling CoreV1Api->create_namespaced_replication_controller: %s\n" % e)

