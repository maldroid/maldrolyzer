from templates import Plugin

class Xbot007(Plugin):
	NAME = 'xbot007'

	def recon(self):
		for s in self.dvm.get_strings():
			if 'xbot007' in s.lower().translate(None, '#%'):
                                return True
                return False

	def extract(self):
		php_end = None
		for string in self.dvm.get_strings():
			if string.endswith('.php'):
				php_end = string
		for cls in self.dvm.get_classes():
			# There has to be a better method to do THIS
			if len(cls.get_methods()) == 1 and\
				cls.get_methods()[0].name == '<clinit>' and\
				len(cls.get_fields()) >= 2 and\
				len(cls.get_fields()) < 10:
				for inst in cls.get_methods()[0].get_instructions():
					if inst.get_name() == 'const-string':
						host = inst.get_output().translate(None, '#%').split(',')[-1].strip("' ")
						break
		result = {'c2': ['http://' + host + '/' + php_end]}
		return result
