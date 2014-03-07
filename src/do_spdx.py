# This class integrates real-time license scanning, generation of SPDX standard
# output and verifiying license info.
#
# For more information on FOSSology:
#   http://www.fossology.org
#
# For more information on FOSSologySPDX commandline:
#   https://github.com/spdx-tools/fossology-spdx/wiki/Fossology-SPDX-Web-API
#
# For more information on SPDX:
#   http://www.spdx.org
# 
# To use this class either import the file and create an instance of the 
# DoSpdx class, or execute the file on the command line with the appropriate
# usage options and parameters.
#
# Licensing information for this file and project can be found in
# /documentation/License

# TODO: Get requirements for configuraiton
# TODO: Identify class members
# TODO: Implement do_spdx

"""

"""
class DoSpdx():
	info = {}
	def __init__(self, info):
		import os
		self.info = info
	def do_spdx(self):
		import os, sys, json
		completed = False

		return completed

	def __create_manifest(self, info, header, files):

	def __get_cached_spdx(self, sstatefile):

	def __write_cached_spdx(self, sstatefile, ver_code, files):
	
	def __setup_foss_scan(self, cache, cached_files):

	def __remove_dir_tree(self, dir_name):

	def __remove_file(self, file_name):

	def __list_files(self, dir):

	def __hash_file(self, file_name):

	def __hash_string(self, data):

	def __run_fossology(self, foss_command):

	def __create_spdx_doc(self, file_info, scanned_files):

	def __get_ver_code(self, dirname):

	def __get_header_info(self, spdx_verification_code, spdx_files):

if __name__ = '__main__':
	run_do_spdx()
		
def run_do_spdx():
	from argparse import ArgumentParser
	from ConfigParser import ConfigParser
	from sys import exit
	# set up base parser
	parser = ArgumentParser(description='Generate spdx documents for the provided tarfile')
	parser.add_argument('package', action='append', type=file, help='Create SPDX for this package; must be tar.gz') # required path to tarball

	# set up subparsers
	subparsers = parser.add_subparsers(title='config method', description='method of configuration')
	config = subparsers.add_parser('c', help='using config file')	# subparser for use of a config file
	config.add_argument('file', type=file, action=append, help='Path to config file')	# path to config file. validate file using ConfigParser
	
	options = subparsers.add_parser('o', dest='', help='using command line options')	# subparser for use of options from command line
	options.add_argument('outfile', action='append', type=file, help='Output file for SPDX after process is finished')	# path to output
	options.add_argument('author', action='append', type=str, help='Author name')	# author name
	options.add_argument('tool', action='append', type=str, help='URL of scanning tool host')	# SPDX version
	options.add_argument('package_name', action='append', type=str, help='Package name')
	options.add_argument('package_version', action='append', type=str, help='Package version')
	options.add_argument('spdx_version', action='append', type=str, help='Which SPDX version to generate')
	options.add_argument('data_license', action='append', type='str', help='License type')
	options.add_argument('spdx_temp_dir', action='append', type=file, help='Temp directory for SPDX generation')
	args = parser.parse_args()	# get the arguments and parameters as key value pairs in args

	info = {}
	info['package'] = args['package']
	if 'file' in vars(args):
		config_parser = ConfigParser.RawConfigParser()
		if args['file'].endswith('.cfg'): 
			config_parser.read(args['file'])
		else:
			print "Invalid file extension."
			exit(1)
		info['author'] = config_parser.get('Settings', 'author')
		info['workdir'] = config_parser.get('Settings', 'workdir')
		info['package_name'] = config_parser.get('Settings', 'package_name')
		info['package_version'] = config_parser.get('Settings', 'package_version')
		info['spdx_version'] = config_parser.get('Settings', 'spdx_version')
		info['outfile'] = config_parser.get('Settings', 'outfile')
		info['tool'] = config_parser.get('Settings', 'tool')
		info['spdx_temp_dir'] = config_parser.get('Settings', 'spdx_temp_dir')
		info['data_license'] = config_parser.get('Settings', 'data_license')
	else:
		info['author'] = args['author']
		info['workdir'] = args['workdir']
		info['package_name'] = args['package_name']
		info['package_version'] = args['package_version']
		info['spdx_version'] = args['spdx_version']
		info['outfile'] = args['outfile']
		info['tool'] = args['tool']
		info['spdx_temp_dir'] = args['spdx_temp_dir']
		info['data_license'] = args['data_license']



	## TODO: Complete config parsing and pass parameters to DoSpdx constructor

	#    info['workdir'] = (d.getVar('WORKDIR', True) or "")
	#    info['sourcedir'] = (d.getVar('S', True) or "")
 	#    info['pn'] = (d.getVar( 'PN', True ) or "")
 	#    info['pv'] = (d.getVar( 'PV', True ) or "")
 	#    info['src_uri'] = (d.getVar( 'SRC_URI', True ) or "")
 	#    info['spdx_version'] = (d.getVar('SPDX_VERSION', True) or '')
 	#    info['data_license'] = (d.getVar('DATA_LICENSE', True) or '')
 	#    spdx_sstate_dir = (d.getVar('SPDXSSTATEDIR', True) or "")
 	#    manifest_dir = (d.getVar('SPDX_MANIFEST_DIR', True) or "")
 	#    info['outfile'] = os.path.join(manifest_dir, info['pn'] + ".spdx" )
 	#    sstatefile = os.path.join(spdx_sstate_dir, 
 	#    info['pn'] + info['pv'] + ".spdx" )
 	#    info['spdx_temp_dir'] = (d.getVar('SPDX_TEMP_DIR', True) or "")
 	#    info['tar_file'] = os.path.join( info['workdir'], info['pn'] + ".tar.gz" )

	mDoSpdx = DoSpdx(info)
	print("Starting creation of spdx documents")
	completed = mDoSpdx.do_spdx()
	if completed:
		print("SPDX generated successfully.")
	else:
		print("SPDX generation unsuccessful.")