from plugins import *
from processing import *
import argparse
from templates import Plugin, OutputProcessor, get_plugin_prevalues
from pprint import pprint

def load_plugins():
	result = [cls for cls in Plugin.__subclasses__()]
	return result

def run_plugins(args, plugins, filename):
	anything = False
	processors = [cls(args) for cls in OutputProcessor.__subclasses__()]
	prevalues = get_plugin_prevalues(args, filename)
	for plugin in plugins:
		plugin = plugin(args, filename, prevalues)
		if plugin.recon():
			anything = True
			data = plugin.extract()
			for processor in processors:
				processor.process(filename, plugin.NAME, data)
	if not anything:
		print 'Sorry, no plugin could handle the file'

def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument("file", type=str,
                    help="file to analyze")
	args = argparser.parse_args()
	plugins = load_plugins()
	run_plugins(args, plugins, args.file)
	

if __name__ == '__main__':
	main()
