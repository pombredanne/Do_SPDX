# Copyright 2014 Corbin Haughawout
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
# Licensing information for Do_SPDX project can be found under
# /documentation/license/LICENSE.txt

import logging
logger = logging.getLogger(__name__)

class DoSpdx():
	"""
	This class manages the creation and storage of spdx documentation into a database.
	Simply call do_spdx after initializing a DoSpdx object and passing it the required arguments.
	"""

	info = {}
	def __init__(self, info):
		'''
		Construct a DoSpdx object with the provided info settings.
		All required settings are validated when do_spdx is called.
		'''
		import os
		self.info = info
		logger.info("Created DoSpdx obejct with info: " + str(info))
	def do_spdx(self):
		'''
		The single entry point for the DoSpdx process.
		TODO: Add details on expections of the process and user input,
		how it validates that input, and what it will output.
		'''
		import os, sys, json
		_validate_configuration()
		logger.info("Starting do_spdx process")
		cur_ver_code = get_ver_code( info['sourcedir'])
		cache_cur = False
		if not os.path.exists( info['spdx_temp_dir'] ):
			os.makedirs(info['spdx_temp_dir'])

#		if package is in database:  check database for package
#			cache_cur = True
#		else:
#			local_file_info = setup_foss_scan( info, True, cached_spdx['Files'])


			
	def _create_manifest(self, info, header, files):

	def _validate_configuration(self):
		logger.info("Starting validation")

	def _get_cached_spdx(self, sstatefile):
		import json, mysql
		stored_spdx_info = {}
		try:
			conn = mysql.connector.connect(user=info['database_user'], password=info['database_password'],
				host=info['database_host'], database=info['database_env'])
			cur = conn.cursor()

		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				log.error("Access denied to database.")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				log.error("Database does not exist.")
			else:
				log.error(str(err))
			exit()
		else:	
			conn.close()

	def _write_cached_spdx(self, sstatefile, ver_code, files):
	
	def _setup_foss_scan(self, cache, cached_files):

	def _remove_dir_tree(self, dir_name):

	def _remove_file(self, file_name):

	def _list_files(self, dir):

	def _hash_file(self, file_name):

	def _hash_string(self, data):

	def _run_fossology(self, foss_command):

	def _create_spdx_doc(self, file_info, scanned_files):

	def _get_ver_code(self, dirname):

	def _get_header_info(self, spdx_verification_code, spdx_files):

class InvalidFileExtensionException(Exception):
	'''This custom Exception is used when the user provides the wrong file type.'''
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


if __name__ = '__main__':
	run_do_spdx()
		
def run_do_spdx():
	'''Run the do_spdx process from the command line. '''
	from argparse import ArgumentParser
	from ConfigParser import ConfigParser
	from sys import exit
	import os.path, logging


	# set up base parser
	parser = ArgumentParser(description='Generate spdx documents for the provided tarfile')
	parser.add_argument('package', action='append', type=file, help='Create SPDX for this package; must be tar.gz') # required path to tarball

	# set up subparsers
	subparsers = parser.add_subparsers(title='config method', description='method of configuration')
	config = subparsers.add_parser('-c', help='using config file')	# subparser for use of a config file
	config.add_argument('file', type=file, action=append, help='Path to config file')	# path to config file. validate file using ConfigParser
	
	options = subparsers.add_parser('-o', dest='', help='using command line options')	# subparser for use of options from command line
	options.add_argument('-f', '--outfile', action='append', type=file, required=False, help='Output file for SPDX after process is finished')	# path to output
	options.add_argument('-a', '--author', action='append', type=str, required=True, help='Author name')	# author name
	options.add_argument('-t', '--tool', action='append', type=str, required=True, help='URL of scanning tool host')	# SPDX version
	options.add_argument('-pn', '--package_name', action='append', type=str, required=True, help='Package name')
	options.add_argument('-pv', '--package_version', action='append', type=str, required=True, help='Package version')
	options.add_argument('-sv', '--spdx_version', action='append', type=str, required=True, help='Which SPDX version to generate')
	options.add_argument('-d', '--data_license', action='append', type='str', required=True, help='License type')
	options.add_argument('-sd', '--spdx_temp_dir', action='append', type=file, required=True, help='Temp directory for SPDX generation')
	args = parser.parse_args()	# get the arguments and parameters as key value pairs in args

	info = {}
	info['tar_file'] = args['package']
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
		if args.author
			info['author'] = args.author
		elif args.a:
			info['author'] = args.a
		info['workdir'] = os.getcwd
		if args.package_name:
			info['package_name'] = args.package_name
		elif args.pn
			info['package_name'] = args.pn
		if args.package_version:
			info['package_version'] = args.package_version
		elif args.pv:
			info['package_version'] = args.pv
		if args.spdx_version:
			info['spdx_version'] = args.spdx_version
		elif args.sv:
			info['spdx_version'] = args.sv
		if args.outfile:	
			info['outfile'] = args.outfile
		elif args.f:
			info['outfile'] = args.f
		else:
			info['outfile'] = ""	# Stdout
		if args.tool:
			info['tool'] = args.tool
		elif args.t:
			info['tool'] = args.t
		if args.spdx_temp_dir:
			info['spdx_temp_dir'] = args.spdx_temp_dir
		elif args.sd:
			info['spdx_temp_dir'] = args.sd
		if args.data_license:
			info['data_license'] = args.data_license
		elif args.d:
			info['data_license'] = args.d

	# Get DoSpdx object with supplied parameters
	mDoSpdx = DoSpdx(info)
	# Run do_spdx process on that object
	completed = mDoSpdx.do_spdx()
	# Output should be for the supplied outfile, or to stdout if not supplied.