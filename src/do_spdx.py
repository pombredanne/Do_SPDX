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
		If settings are invalid, object initialization fails and
		the system aborts the object creation.
		'''
		import os
		self.info = info
		_validate_configuration()
		logger.debug("Created DoSpdx obejct with info: " + str(info))

	def do_spdx(self):
		'''
		The single entry point for the DoSpdx process.
		TODO: Add details on expections of the process and user input,
		how it validates that input, and what it will output.
		'''
		import os, sys, json, tarfile
		logger.info("Starting do_spdx process")



		# check if package is in staging directory
		install_path = os.path.abspath("../do_spdx/staging/" + info['package'])

		if not os.path.exists(install_path):	# if path does not exist
			logger.error("Package not in staging directory. Stopping process.")

		# package exists, so extract the package to the staging directory
		# and sha1 it
		tar = tarfile.open(install_path, 10240, "r:gz")

		tar.extractall("../do_spdx/staging/")
		tar.close()

		# get the package name without .tar.gz extension for hashing
		extracted = os.path.splitext(info['package'])

		file_hash = _hash_file(extracted)

		# check if package checksum matches a row in database
		in_database = False
		file_list = {}
		if not _file_in_database(file_hash):
			file_list = _setup_foss_scan(extracted)
		else:
			in_database = True
		

	def _setup_foss_scan(self, file_name):
		'''
		Set up the requirements for the fossology scan. Gather all unknown files
		for scanning and all known files, return both lists.
		'''
		import errno, shutil, tarfile, os

		full_file_paths = []
		# get all files whose checksum does not match in database
		# then send to fossology for scanning
		full_file_paths = _get_filepaths(file_name)
		checksums = _get_checksums_for_list(full_file_paths)



	def _get_checksums_for_list(files):
		'''
		Get all sha1's of the 
		'''
		checksums = {}
		for f in full_file_paths:
			checksums[f] = _hash_file(f)

		return checksums

	def _get_filepaths(directory):
		"""
	    This function will generate the file names in a directory 
	    tree by walking the tree either top-down or bottom-up. For each 
	    directory in the tree rooted at directory top (including top itself), 
	    it yields a 3-tuple (dirpath, dirnames, filenames).
	    """
	    file_paths = []  # List which will store all of the full filepaths.

	    # Walk the tree.
	    for root, directories, files in os.walk(directory):
	        for filename in files:
	            # Join the two strings in order to form the full filepath.
	            filepath = os.path.join(root, filename)
	            file_paths.append(filepath)  # Add it to the list.

	    return file_paths  # Self-explanatory.

	def _hash_file(file_path):
		try:
			f = open(file_path, 'rb')
			data_string = f.read()
		except:
			return None
		finally:
			f.close()
		sha1 = _hash_string(data_string)
		return sha1

	def _hash_string(data):
		from hashlib import sha1
		file_sha1 = sha1()
		file_sha1.update(data)
		return file_sha1.hexdigest()

	def _file_in_database(self, sha1):
		import mysql, json
		logger.info("Querying database")
		# procedure is something like select * from packages where package_checksum = package_cs
		con = mysql.connector.connect(user=info['database_user'], password=info['database_password'], 
			host=['database_host'], database=['database_name'])
		with con:
			logger.debug("Connection succeeded, querying")
			cur = con.cursor()
			logger.debug("Query: SELECT * FROM " + table + " WHERE " + my_type + "_checksum = " + package_cs)
			# TODO: Change this to be a stored procedure or at least to a prepared statement.
			cur.execute("SELECT * FROM packages WHERE package_checksum = " + sha1)
			rows = cur.fetchall()
			con.close()
			if rows:
				return True
			else:
				return None

	def _create_manifest(self, header, files):
		'''
		Create the manifest containing the license information returned
		from the scanner(s). The manifest is output to the outfile provided
		by the user, stdout if none is provided. The header 
		'''
	    with open(info['outfile'], 'w') as f:
        f.write(header + '\n')
        for chksum, block in files.iteritems():
            for key, value in block.iteritems():
                f.write(key + ": " + value)
                f.write('\n')
            f.write('\n')

	def _get_header_info(self, spdx_verification_code, spdx_files):
		"""
        Put together the header SPDX information.
        Eventually this needs to become a lot less
        of a hardcoded thing.
		"""
		from datetime import datetime
		import os
		head = []
		DEFAULT = "NOASSERTION"

		#spdx_verification_code = get_ver_code( info['sourcedir'] )
		package_checksum = ''
		if os.path.exists(info['tar_file']):
		    package_checksum = hash_file( info['tar_file'] )
		else:
		    package_checksum = DEFAULT

		## document level information
		head.append("SPDXVersion: " + info['spdx_version'])
		head.append("DataLicense: " + info['data_license'])
		head.append("DocumentComment: <text>SPDX for "
		    + info['pn'] + " version " + info['pv'] + "</text>")
		head.append("")

		## Creator information
		now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
		head.append("## Creation Information")
		head.append("Creator: fossology-spdx")
		head.append("Created: " + now)
		head.append("CreatorComment: <text>UNO</text>")
		head.append("")

		## package level information
		head.append("## Package Information")
		head.append("PackageName: " + info['pn'])
		head.append("PackageVersion: " + info['pv'])
		head.append("PackageDownloadLocation: " + DEFAULT)
		head.append("PackageSummary: <text></text>")
		head.append("PackageFileName: " + os.path.basename(info['tar_file']))
		head.append("PackageSupplier: Person:" + DEFAULT)
		head.append("PackageOriginator: Person:" + DEFAULT)
		head.append("PackageChecksum: SHA1: " + package_checksum)
		head.append("PackageVerificationCode: " + spdx_verification_code)
		head.append("PackageDescription: <text>" + info['pn']
		    + " version " + info['pv'] + "</text>")
		head.append("")
		head.append("PackageCopyrightText: <text>" + DEFAULT + "</text>")
		head.append("")
		head.append("PackageLicenseDeclared: " + DEFAULT)
		head.append("PackageLicenseConcluded: " + DEFAULT)
		head.append("PackageLicenseInfoFromFiles: " + DEFAULT)
		head.append("")

		## header for file level
		head.append("## File Information")
		head.append("")

		return '\n'.join(head)

class InvalidFileExtensionException(Exception):
	'''This custom Exception is used when the user provides the wrong file type.'''
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Only run run_do_spdx if the module was called from command line
if __name__ = '__main__':
	run_do_spdx()
		
def run_do_spdx():
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