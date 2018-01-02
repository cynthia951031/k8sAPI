k8sAPI by python client

1. 关于 flask 的 request 请求数据解析：

    在 requests 端：
     request(url, json = login_data)
    在restful端:

        print "received..."
        print request.cookies
        print request.form
        print request.data
        print type(request.data)
        print request.json
        print type(request.json)
    result:
        received...
    	{}
    	ImmutableMultiDict([])
    	{"id": 123, "name": "abc"}
    	<type 'str'>
    	{u'id': 123, u'name': u'abc'}
    	<type 'dict'>

2. instance detail 包括：
    id
    name
    cpu
    memory
    gpu #这个不太清楚在哪里创建自然也不知道怎么查询
    service ip
    isSSD
    create time
    deletion time
    update time
    service ports

3. 包括 两种 创建方式 
    @所有 deployment 都是 extension/v1beta版本的 api，是一种新型 rc
    @另外一种是 rc 和 service 都创建，API 版本： corev1
    ***再用不同的方式的时候记得在__init__.py 中改变 api 版本