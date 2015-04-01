from androguard.core.bytecodes import dvm, apk
from androguard.core.analysis import analysis
from zipfile import ZipFile

def get_plugin_prevalues(args, filename):
	result = {}
	a = apk.APK(filename)
	result['apk'] = a
	result['dvm'] = dvm.DalvikVMFormat(a.get_dex())
	result['dx'] = analysis.VMAnalysis(result['dvm'])
	result['zipfile'] = ZipFile(filename)
	return result
	

class Plugin(object):
	NAMES = []

	def __init__(self, args, filename, prevalues={}):
		self.filename = filename
		self.args = args
		self.dvm = self.apk = None
		for name, value in prevalues.iteritems():
			setattr(self, name, value)

	def recon(self):
		return False

	def extract(self):
		pass

class OutputProcessor(object):
	def __init__(self, args):
		self.args = args

	def process(self, filename, data):
		pass

class Collector(object):
	def __init__(self, args):
		self.args = args

	def get_samples(self):
		pass
