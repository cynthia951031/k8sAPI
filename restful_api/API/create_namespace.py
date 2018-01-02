from kubernetes import client
from . import configuration
from kubernetes.client.rest import ApiException

def create_namespace_object(namespace_name):
	metadata = client.V1ObjectMeta(name = namespace_name, 
									labels = dict(name=str(namespace_name)))
	namespace = client.V1Namespace(api_version = "corev1", 
									kind = "Namespace", 
									metadata = metadata)
	return namespace

def create_namespace(namespace_object):
	api_instance = client.CoreV1Api(kubernetes.client.ApiClient(configuration))
	pretty = 'True'
	try:
		api_response = api_instance.create_namespace(body=namespace_object, 
													pretty=pretty)
	except ApiException as e:
		print("Exception when calling CoreApi->create_namespace: %s \n" % e)
	return api_response
