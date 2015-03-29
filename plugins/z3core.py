from templates import Plugin
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from cStringIO import StringIO
import gzip, string, re

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
				'mscorlib_dll', 'System_dll',
				]

	def recon(self):
		z = ZipFile(self.filename)
		if not 'lib/armeabi-v7a/libmonodroid.so' in z.namelist() or not 'lib/armeabi-v7a/libmonodroid_bundle_app.so' in z.namelist():
			return False
		f = z.open('lib/armeabi-v7a/libmonodroid_bundle_app.so')
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
		data = z.open('lib/armeabi-v7a/libmonodroid_bundle_app.so').read()
		f = StringIO(data)
		elffile = ELFFile(f)
		section = elffile.get_section_by_name('.dynsym')
		for symbol in section.iter_symbols():
			if symbol['st_shndx'] != 'SHN_UNDEF' and symbol.name.startswith('assembly_data_'):
				if symbol.name[14:] in self.WHITELISTED_DLL:
					continue
				dll_data = data[symbol['st_value']:symbol['st_value']+symbol['st_size']]
				dll_data = gzip.GzipFile(fileobj=StringIO(dll_data)).read()
				regexp = 'h\x00t\x00t\x00p\x00:\x00/\x00/\x00.*?\x00\x00'
				s = map(lambda x : x.replace('\x00',''), re.compile(regexp, flags=re.UNICODE).findall(dll_data))
				c2.extend(s)
		return {'c2': c2}

