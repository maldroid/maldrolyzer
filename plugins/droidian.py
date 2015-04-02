from templates import Plugin
import base64

class Droidian(Plugin):

	NAME = 'droidian'

	def recon(self):
		for cls in self.dvm.get_classes():
			if cls.name.lower().endswith('droidianservice;'):
				self.droidian_service = cls
				return True
		return False
		
	def extract(self):
		hosts = set()
		string = None
		for method in self.droidian_service.get_methods():
			if method.name == '<init>':
				for inst in method.get_instructions():
					if inst.get_name() == 'const-string':
						string = inst.get_output().split(',')[-1].strip(" '")
						try:
							string = base64.b64decode(string)
						except:
							string = None
					elif string and inst.get_name() == 'iput-object' and inst.get_output().split('->')[-1].startswith('encodedURL') or inst.get_output().split('->')[-1].startswith('backupURL'):
						hosts.add(string)
						
		return {'c2': list(hosts)}
