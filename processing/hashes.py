from templates import OutputProcessor
import hashlib

class Hashes(OutputProcessor):
	def process(self, filename, data):
		data = open(filename).read()
		result = {}
		result['md5'] = hashlib.md5(data).hexdigest()
		result['sha256'] = hashlib.sha256(data).hexdigest()
		result['sha1'] = hashlib.sha1(data).hexdigest()
		result['sha512'] = hashlib.sha512(data).hexdigest()
		return result
