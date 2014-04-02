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
		# TODO: Handle _validate_configuration
		_validate_configuration()
		_init_logging_config()
		logger.debug("Created DoSpdx obejct with info: " + str(info))

	def _validate_configuration():
		'''
		Ensures that the expected required parameters are valid and that users have the required permissions.
		'''
		# TODO Implementation
		pass

	def _init_logging_config():
		'''
		Initialize the logging for this Do_SPDX module from the configuration file provided.
		'''
		# TODO Implementation

		pass

	def do_spdx(self):
		'''
		The single entry point for the DoSpdx process.
		TODO: Add details on expections of the process and user input,
		how it validates that input, and what it will output.
		'''
		import os, sys, json, tarfile, random
		logger.info("Starting do_spdx process")

		# Get the hash of the tar file by passing it to the _hash_file function
		package_hash = _hash_file(info['package'])

		# Check if package is in database
		if _file_in_database(package_hash):
			logger.info("Package checksum exists in database")
			if info['force']:
				logger.info('Forcing re-scan of package')
			else:	
				if info['quiet']:
					logger.info("Exiting without output")
					sys.exit(0)		# Exited quietly
				else:
					logger.info("Creating output then terminating")
					package_files = _get_package_files(package_hash)
					header = _get_header_info(info, package_hash)
					_create_manifest(header, package_files, info['quiet'])
					sys.exit(0)		# Exited with output

		# get temporary directory for staging purposes
		tmpdir = os.path.join(info['spdx_temp_dir'], 'do_spdx')

		if not os.path.exists(tmpdir):
			os.mkdir(tmpdir)

		# Unpack to tmpdir
		tar = tarfile.open(info['package'], 'r:gz')
		tar.extractall(tmpdir)
		tar.close()

		package_id = _get_package_id(package_checksum)

		if not _file_in_database(file_hash):
			to_scan, no_scan = _setup_foss_scan(package_id)
		else:
			in_database = True


	def _cleanup(self):
		# TODO clean up the tmp files from the tmp directory
		pass

	def _get_package_id(self, package_checksum):
		'''
		@return the id belonging to the package checksum
		'''

		import MySQLdb
		con = mysql.connect(user=info['database_user'], password=info['database_password'], 
			host=['database_host'], database=['database_name'])
		with con:
			cur = con.cursor()
			sql = "SELECT id from packages WHERE package_checksum == " + package_checksum
			cur.execute()
			rows = cur.fetchall()
			return rows[0]

	def _get_package_files(self, package_checksum):
		'''
		Creates a list of files that are different for the package and files that are
		in the package and valid then returns both lists.
		'''
		import MySQLdb
		package_files = {}


	def _setup_foss_scan(self, package_id):
		'''
		Set up the requirements for the fossology scan. Gather all unknown files
		for scanning and all known files, return both lists.
		'''
		import os, MySQLdb

		full_file_paths = []
		# get all files whose checksum does not match in database
		# then send to fossology for scanning
		full_file_paths = _get_filepaths(file_name)
		file_checksums = _get_checksums_for_list(full_file_paths)
		checksums = []
		for key in file_checksums.keys():
			checksums.append(file_checksums[key])

		# use checksums in query and construct two lists,
		# one containing files to scan, the other files that
		# are in database
		no_scan, to_scan = [], []
		con = mysql.connect(user=info['database_user'], password=info['database_password'], 
			host=['database_host'], database=['database_name'])
		with con:
			cur = con.cursor()
			sql = "SELECT * FROM doc_file_package_assocations WHERE file_checksum in (%s)"
			in_p = ', '.join(map(lambda x: '%s', checksums))
			sql = sql % in_p
			cur.execute(sql, checksums)
			rows = cur.fetchall()
			for path, checksum in file_checksums.items():
				if checksum 

	def _get_checksums_for_list(files):
		'''
		Get all sha1's of the staged files.
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

		return file_paths  

	def _hash_file(file_path):
		'''
		A location independent checksum generator that generates a sha1
		of the contents of the file provided. Used in Do_SPDX to 
		provide a so-called PackageVerificationCode so that the user
		may detect if a package already has SPDX generated for it.
		'''
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
		'''
		This hashing function accepts some data as a string and runs it through the sha1
		hashing algorithm. Returns the hexdigest of the data to the caller.
		This function is called from within the private _hash_file method of the Do_SPDX
		module.
		'''
		from hashlib import sha1
		file_sha1 = sha1()
		file_sha1.update(data)
		return file_sha1.hexdigest()

	def _file_in_database(self, sha1):
		import MySQLdb, json
		logger.info("Querying database")

		# procedure is something like select * from packages where package_checksum = package_cs
		con = mysql.connect(user=info['database_user'], passwd=info['database_password'], 
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

	def _create_manifest(self, header, files, quiet):
		'''
		Create the manifest containing the license information returned
		from the scanner(s). The manifest is output to the outfile provided
		by the user, stdout if none is provided.
		'''
		from sys import stdout

		# Construct manifest
		to_file = header + '\n'
		for chksum, block in files.iteritems():
			for key, value in block.iteritems():
				to_file += key + ": " + value
				to_file += '\n'
			to_file += '\n'

		# Only output if quiet is not enabled
		if not quiet:
			with open(info['outfile'], 'w') as f:
				f.write(to_file)	# write to file
				if f is not stdout:	# output to command line if not already
					print to_file
		# END of _create_manifest()

	def _get_header_info(self, spdx_verification_code):
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

# Only execute run_do_spdx if the module was called from command line
if __name__ = '__main__':
	run_do_spdx()
		
def run_do_spdx():
	from argparse import ArgumentParser
	from ConfigParser import ConfigParser
	from sys import exit
	import os.path


	# Set up base parser
	parser = ArgumentParser(description='Generate spdx documents for the provided tarfile')
	parser.add_argument('package', action='append', required=True, type=file, help='Create SPDX for this package') # required, path to package
	parser.add_argument('cfg', action='append', required=True, type=file, help='Supply a valid configuration file')	# required, path to configuration file
	parser.add_argument('-q', '--quiet', action='append', required=False, help='Mute the file and stdout output of Do_SPDX')	# optional, quiet output
	parser.add_argument('-f', '--force', action='append', required=False, help='Force Do_SPDX to scan the package and update the database with its SPDX') # optional, force update
	args = parser.parse_args()	# get the arguments and parameters as key value pairs in args

	# Start Settings
	info = {}
	info['tar_file'] = args.package
	info['config_path'] = args.cfg
	if args.quiet:
		info['quiet'] = args.quiet
	if args.force:
		info['force'] = args.force
	configParser = ConfigParser.RawConfigParser()
	configParser.read(info['config_path'])

	# Getting General Settings for Do_SPDX
	info['author'] = configParser.get('Settings', 'author')
	info['spdx_temp_dir'] = configParser.get('Settings', 'spdx_temp_dir')
	info['spdx_version'] = configParser.get('Settings', 'spdx_version')
	info['outfile'] = configParser.get('Settings', 'outfile')
	info['tool'] = configParser.get('Settings', 'tool')

	# Getting Database Settings for Do_SPDX
	info['database_user'] = configParser.get('Database', 'database_user')
	info['database_name'] = configParser.get('Database', 'database_name')
	info['database_host'] = configParser.get('Database', 'database_host')
	info['database_port'] = configParser.get('Database', 'database_port')
	info['database_password'] = configParser.get('Database', 'database_password')

	# Get DoSpdx object with supplied parameters
	mDoSpdx = DoSpdx(info)
	# Run do_spdx process on that object
	completed = mDoSpdx.do_spdx()
	# Output should be for the supplied outfile, or to stdout if not supplied.