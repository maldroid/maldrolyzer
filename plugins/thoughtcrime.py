from templates import Plugin
from zipfile import ZipFile
import base64
from Crypto.Cipher import Blowfish
import xml.etree.ElementTree as ET

class Thoughtcrime(Plugin):
	NAME = "thoughtcrime"

	def recon(self):
		return 'res/raw/blfs.key' in self.zipfile.namelist() and \
			'res/raw/config.cfg' in self.zipfile.namelist()

	def extract(self):
		raw_resources = filter(lambda x: x.startswith('res/raw'), self.zipfile.namelist())
		iv = "12345678" # this has to be done better
		key = self.zipfile.open('res/raw/blfs.key').read()
		key = ''.join(['%x' % ord(x) for x in key])[0:50]
		cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
		decode = base64.b64decode(self.zipfile.open('res/raw/config.cfg').read())
		config = cipher.decrypt(decode)
		config = config[:config.find('</config>')+9]
		config = ET.fromstring(config)
		c2 = config.findall('.//data')[0].get('url_main').split(';')
		phone = config.findall('.//data')[0].get('phone_number')
		return {'c2': c2, 'phone': phone}

