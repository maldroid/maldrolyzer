from templates import Plugin
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from cStringIO import StringIO
import gzip, string
import yara

def get_strings(data):
	result = ""
	for c in data:
		if c in string.printable:
			result += c
			continue
		if len(result) >= 8:
			yield result
		result = ""

class Z3Code(Plugin):

	NAME = 'Z3Core'

	WHITELISTED_DLL = ['System_Core_dll', 'NLua_Android_dll', 
				'KopiLua_Android_dll', 'Mono_Android_dll', 
				'Z_VFS_Android_dll', 'Xamarin_Mobile_dll',
				'mscorlib_dll', 'System_dll', 'Mono_Android_Export_dll',
				'System_Xml_dll'
				]

	def recon(self):
		z = ZipFile(self.filename)
		bundle = False
		if 'lib/armeabi-v7a/libmonodroid.so' in z.namelist() and 'lib/armeabi-v7a/libmonodroid_bundle_app.so' in z.namelist():
			bundle = 'lib/armeabi-v7a/libmonodroid_bundle_app.so'
		elif 'lib/armeabi/libmonodroid.so' in z.namelist() and 'lib/armeabi/libmonodroid_bundle_app.so' in z.namelist():
			bundle = 'lib/armeabi/libmonodroid_bundle_app.so'
		if not bundle:
			return False
		self.bundle = bundle
		f = z.open(bundle)
		f = StringIO(f.read())
		elffile = ELFFile(f)
		section = elffile.get_section_by_name('.dynsym')
		for symbol in section.iter_symbols():
			if symbol['st_shndx']  != 'SHN_UNDEF' and symbol.name == 'mono_mkbundle_init':
				return True
        	return False

	def extract(self):
		c2 = []
		z = ZipFile(self.filename)
		data = z.open(self.bundle).read()
		f = StringIO(data)
		elffile = ELFFile(f)
		section = elffile.get_section_by_name('.dynsym')
		for symbol in section.iter_symbols():
			if symbol['st_shndx'] != 'SHN_UNDEF' and symbol.name.startswith('assembly_data_'):
				if symbol.name[14:] in self.WHITELISTED_DLL:
					continue
				dll_data = data[symbol['st_value']:symbol['st_value']+symbol['st_size']]
				dll_data = gzip.GzipFile(fileobj=StringIO(dll_data)).read()
				regexp = """rule find_url { 
							strings: 
							$url = /http:\/\/[A-Za-z0-9\.\/$\-_+!\*'(),]*/ wide 
							condition: 
							$url}"""
				compiled = yara.compile(source = regexp)
				s = compiled.match(data = dll_data)
				for entry in s['main'][0]['strings']:
					cc = dll_data[entry['offset']:entry['offset']+len(entry['data'])].decode('utf-16')
					c2.append(cc)
		return {'c2': c2}

