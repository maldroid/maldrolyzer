from templates import Plugin

class Marcher(Plugin):

	NAME = 'Marcher'

	def recon(self):
		for s in self.dvm.get_strings():
			if s.startswith('get.php'):
				self.gate = s
				return True

	def extract(self):
		tainted = self.dx.get_tainted_variables().get_string(self.gate)
		m_idx = tainted.get_paths()[0][1]
		url_cls = self.dvm.get_cm_method(m_idx)[0]
		for cls in self.dvm.get_classes():
			if cls.name == url_cls:
				url_cls = cls.get_superclassname()
				break
		for cls in self.dvm.get_classes():
			if cls.name == url_cls:
				for method in cls.get_methods():
					if method.name == '<init>':
						for inst in method.get_instructions():
							if inst.get_name() == 'const-string':
								c2 = inst.get_output().split(',')[-1].strip("' ")
		return {'c2': [c2 + self.gate]}

