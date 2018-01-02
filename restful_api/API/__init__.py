#! /usr/bin/env python
# -*- coding: utf-8 -*-


from kubernetes import client

KUBE_TOKEN = 'KUBE_TOKEN...FILL_IT_LATER...'
configuration = client.Configuration()
configuration.api_key['authorization'] = KUBE_TOKEN

#different api version
#api_instance = client.ExtensionsV1beta1Api(client.ApiClient(configuration))
api_instance = client.CoreV1Api(client.ApiClient(configuration))
