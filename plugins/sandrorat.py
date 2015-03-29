from templates import Plugin

class Sandrorat(Plugin):
	NAME = 'Sandrorat'

	def recon(self):
		d = self.dvm
		for s in d.get_strings():
			if 'sandrorat' in s.lower() or 'droidjack' in s.lower():
				return True
		return False

	def extract(self):
		d = self.dvm
		c2 = []
		port = []
		for cls in d.get_classes():
			if len(cls.get_fields()) == 3 and\
				set(['a', 'b', 'c']) == set(map(lambda x: x.name, cls.get_fields())) and\
				len(cls.get_methods()) == 1 and\
				cls.get_methods()[0].name.endswith('<clinit>'):
				clinit = cls.get_methods()[0]
				cc = []
				for inst in clinit.get_instructions():
					if inst.get_name() == 'const-string':
						c2.append(inst.get_output().split(',')[-1].strip(" '"))
					elif inst.get_name() == 'const/16':
						port.append(int(inst.get_output().split(',')[-1].strip(" '")))
		servers = []
		for i, server in enumerate(c2):
			if len(port) > i:
				servers.append(server + ':' + str(port[i]))
			else:
				servers.append(server)
		return {'c2': servers}

