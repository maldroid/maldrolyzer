from templates import OutputProcessor
import hashlib
from pprint import pprint

class Hashes(OutputProcessor):
	def process(self, filename, name, data):
		filedata = open(filename).read()
		result = {'malware': name}
		result['md5'] = hashlib.md5(filedata).hexdigest()
		result['sha256'] = hashlib.sha256(filedata).hexdigest()
		result['sha1'] = hashlib.sha1(filedata).hexdigest()
		result['sha512'] = hashlib.sha512(filedata).hexdigest()
		if data:
			result.update(data)
		pprint(result)
