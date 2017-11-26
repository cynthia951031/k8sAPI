from datetime import datetime
from . import db

class Instance(db.model):
	__tabelname__ = 'instance'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(128), nullable=False)
	CPUsize = db.Column(db.Integer, nullable=False)
	MEMsize = db.Column(db.Float, nullable=False)
	GPUnum = db.Column(db.Integer, nullable=False)
	scale = db.Column(db.Integer, nullable=False) # the scale of pods
	isSSD = db.Column(db.Boolean, default=True, nullable=False)
	postStamp = db.Column(db.DataTime)
	serviceIP = db.Column(db.Text)
	servicePort = db.Column(db.Integer)
	updateStamp = db.Column(db.DataTime)
	deleteStamp = db.Column(db.DataTime)


def param_to_model(instance_name, instance_id, cpu, mem, gpu, scale, isSSD):
	instance = Instance()
	instance.id = instance_id
	instance.name = instance_name
	instance.CPUsize = cpu
	instance.GPUnum = gpu
	instance.MEMsize = mem
	instance.scale = scale
	#rest attribute can be optional fill
	return instance

def instance_to_json(ins):
	return json.dumps(dict(instance_name = ins.name),
						   instance_id = ins.id,
						   cpu = ins.CPUsize,
						   gpu = ins.GPUnum,
						   scale = ins.scale,
						   isSSD = ins.isSSD)
