from datetime import datetime
from . import db
from time import time
import jwt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class K8SUser(db.Model):
	__tabelname__ = 'k8suser'
	name = db.Column(db.String(128), nullable=False)
	id = db.Column(db.Integer, primary_key=True)
	namespace = db.Column(db.String(128))

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.avatar_hash is None and self.name is not None:
			self.avatar_hash = hashlib.md5(self.name.encode('utf-8')).hexdigest()
		return

	def get_token(self, expiration = 300):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'name':self.name, 'id':self.id}).decode('utf-8')
	
	@staticmethod
	def validate_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		id = data.get('id')
		name = data.get('name')
		if id:
			return K8SUser.query.get(id)
		return None

class Instance(db.Model):
	__tabelname__ = 'instance'
	name = db.Column(db.String(128), nullable = False)
	id = db.Column(db.Integer, primary_key = True)

def instance_to_json(ins):
	return json.dumps(dict(instance_name = ins.name,
						   instance_id = ins.id,
						   cpu = ins.CPUsize,
						   gpu = ins.GPUnum,
						   scale = ins.scale,
						   isSSD = ins.isSSD))

