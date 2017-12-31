from kubernetes import client
from . import configuration
from kubernetes.client.rest import ApiException

def create_namespace_object(NAMESPACE_NAME):
	metadata = client.V1ObjectMeta(name = NAMESPACE_NAME, 
									labels = dict(name=str(NAMESPACE_NAME)))
	namespace = client.V1Namespace(api_version = "v1", 
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
