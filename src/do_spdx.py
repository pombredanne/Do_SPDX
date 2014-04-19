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
		self.info = info
		# TODO: Handle _validate_configuration
		self._validate_configuration()
		self._init_logging_config()
		logger.debug("Created DoSpdx obejct with info: " + str(info))

	def _validate_configuration(self):
		'''
		Ensures that the expected required parameters are valid and that users have the required permissions.
		'''
		# TODO Implementation
		
		pass

	def _init_logging_config(self):
		'''
		Initialize the logging for this Do_SPDX module from the configuration file provided.
		'''
		import datetime
		logging.config.fileConfig(self.info['config_path'])
		logger = logging.getLogger()
		logger.debug("Logger initialized for Do_SPDX process @" + datetime.datetime.utcnow())

	def do_spdx(self):
		'''
		The single entry point for the DoSpdx process.
		TODO: Add details on expectations of the process and user input,
		how it validates that input, and what it will output.
		'''
		import os, sys, tarfile
		logger.info("Starting do_spdx process")

		# Get the hash of the tar file by passing it to the _hash_file function
		package_hash = self._hash_file(self.info['package'])

		# Check if package is in database
		if self._file_in_database(package_hash):
			logger.info("Package checksum exists in database")
			if self.info['force']:
				logger.info('Forcing re-scan of package')
			else:	
				if self.info['quiet']:
					logger.info("Exiting without output")
					sys.exit(0)		# Exited quietly
				else:
					logger.info("Creating output then terminating")
					package_files = self._get_package_files(package_hash)
					header = self._get_header_info(self.info, package_hash)
					self._create_manifest(header, package_files, self.info['quiet'])
					sys.exit(0)		# Exited with output

		# get temporary directory for staging purposes
		tmpdir = os.path.join(self.info['spdx_temp_dir'], 'do_spdx')

		if not os.path.exists(tmpdir):
			os.mkdir(tmpdir)

		unpacked_package_location = None
		# Unpack to tmpdir
		with tarfile.open(self.info['package'], 'r:gz') as tar:
			tar.extractall(tmpdir)
			unpacked_package_location = os.path.splitext(self.info['package'])
			
		# check if package checksum is in database and return id if it is

		package_id = self._get_package_id(self.package_checksum)
		not_matched, matched = list(), list()
		if package_id:
			not_matched, matched = self._get_package_files(package_id, unpacked_package_location)
		else:
			for root, dirs, files in os.walk(unpacked_package_location):
				not_matched = files

		foss_command = "wget %s --post-file=%s %s"\
			% (self.info['fossology_flags'], not_matched, self.info['fossology_server'])

		foss_file_info =self._run_fossology(foss_command)

		spdx_file_info = self._create_spdx_doc(matched, foss_file_info)



		# if not _file_in_database(file_hash):
		# 	to_scan, no_scan = _setup_foss_scan(package_id)
		# else:
		# 	in_database = True

		self._cleanup()


	def _run_fossology(self, command):
		'''
		Creates a subprocess and executes the Fossology command and returns the
		license information of each file passed to Fossology in a single list.
		'''
		import string, re, subprocess

		p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		foss_output = p.communicate()

		records = re.findall('FileName:.*?</text>', foss_output, re.S)	# a list

		file_info = {}
		for rec in records:
			rec = string.replace( rec, '\r', '' )
			chksum = re.findall( 'FileChecksum: SHA1: (.*)\n', rec)[0]
			file_info[chksum] = {}
			file_info[chksum]['FileCopyrightText'] = re.findall( 'FileCopyrightText: '
	            + '(.*?</text>)', rec, re.S )[0]	            

		fields = ['LicenseDeclared','LicenseInfoInFile','FileName']		# LicenseDeclared, FileName, LicenseComments

		for field in fields:
			file_info[chksum][field] = re.findall(field + ': (.*)', rec)[0]

		return file_info

	def _cleanup(self):
		'''
		Remove all contents of spdx_temp_dir and close any open resources
		'''
		# TODO clean up the tmp files from the tmp directory
		pass

	def _get_package_id(self, package_checksum):
		'''
		@return the id belonging to the package checksum
		'''

		import MySQLdb as mysql
		con = mysql.connect(user=self.info['database_user'], password=self.info['database_password'], 
			host=self.info['database_host'], database=self.info['database_name'])
		with con:
			cur = con.cursor()
			sql = "SELECT id from packages WHERE package_checksum == " + package_checksum
			cur.execute()
			rows = cur.fetchall()
			if rows is not None:	# query returned a package whose checksum matches
				return rows[0]
			else:
				return False

	def _get_package_files(self, package_id, unpacked_package_location):
		'''
		Creates a list of files that are different for the package and files that are
		in the package and valid then returns both lists.
		'''
		import MySQLdb as mysql, os.path, os.walk
		con = mysql.connect(user=self.info['database_user'], password=self.info['database_password'],
			host=self.info['database_host'], database=self.info['database_name'])
		with con:
			cur = con.cursor()
			find_files = "SELECT package_file_id FROM doc_file_package_assocations WHERE package_id == " + package_id 	# get all package_file_ids related to the package_id
			cur.execute(find_files)
			package_file_rows = cur.fetchall()
			get_file_names = "SELECT relative_path FROM package_files WHERE id IN (\'" + str(', '.join(package_file_rows)) + "\')"	# get all relative paths of files in the database for the given package
			cur.execute(get_file_names)
			file_name_paths = cur.fetchall()
			file_name_paths = [os.path.join(unpacked_package_location, location) for location in file_name_paths]
			not_matched, matched = list(), list()
			for root, dirs, files in os.walk(unpacked_package_location, topdown=True):
				for name in files:
					if name not in file_name_paths:
						not_matched.append(name)
					if name in file_name_paths:
						matched.append(name)

			return not_matched, matched

	def _get_checksums_for_list(self, files):
		'''
		Get all sha1's of the staged files.
		'''
		checksums = {f:self._hash_file(f) for f in files}
		return checksums

	def _get_filepaths(self, directory):
		"""
		This function will generate the file names in a directory
		tree by walking the tree either top-down or bottom-up. For each
		directory in the tree rooted at directory top (including top itself),
		it yields a 3-tuple (dirpath, dirnames, filenames).
		"""
		import os
		file_paths = []  # List which will store all of the full filepaths.

		# Walk the tree.
		for root, directories, files in os.walk(directory):
		    for filename in files:
		        # Join the two strings in order to form the full filepath.
		        filepath = os.path.join(root, filename)
		        file_paths.append(filepath)  # Add it to the list.

		return file_paths  

	def _hash_file(self, file_path):
		'''
		A location independent checksum generator that generates a sha1
		of the contents of the file provided. Used in Do_SPDX to 
		provide a so-called PackageVerificationCode so that the user
		may detect if a package already has SPDX generated for it.
		'''
		with open(file_path, 'rb') as f:
			data_string = f.read()
			sha1 = self._hash_string(data_string)
		return sha1

	def _hash_string(self, data):
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
		import MySQLdb as mysql
		logger.info("Querying database")

		# procedure is something like select * from packages where package_checksum = package_cs
		con = mysql.connect(user=self.info['database_user'], passwd=self.info['database_password'], 
			host=self.info['database_host'], database=self.info['database_name'])
		with con:
			logger.debug("Connection succeeded, querying")
			cur = con.cursor()
			logger.debug("Query: SELECT * FROM packages WHERE package_checksum == " + sha1)
			# TODO: Change this to be a stored procedure or at least to a prepared statement.
			cur.execute("SELECT * FROM packages WHERE package_checksum = " + sha1)
			rows = cur.fetchall()
			if rows:
				return True
			else:
				return None
				
	def _create_spdx_doc(self, file_info):
		'''
		Inserts file information about the package into the database
		'''
		import MySQLdb as mysql, time
		logger.info("Inserting into database")
		
		# procedure will insert file information from the scanning utility into the database
		con = mysql.connect(user=self.info['database_user'], passwd=self.info['database_password'], 
			host=self.info['database_host'], database=self.info['database_name'])
		with con:
			logger.debug("Connection succeeded, inserting")
			cur = con.cursor()
			logger.debug("INSERT alot INTO table")
			for checksum in file_info.keys():
				info = {}
				info['FileName'] = file_info[checksum]['FileName']
				info['FileType'] = file_info[checksum]['FileType']
				info['Checksum'] = checksum
				info['LicenseInfoInFile'] = file_info[checksum]['LicenseInfoInFile']
				info['LicenseConcluded'] = file_info[checksum]['LicenseConcluded']
				info['FileCopyrightText'] = file_info[checksum]['FileCopyrightText']
				info['Artifact'] = 'NOASSERTION'
				info['RelativePath'] = 'PUTRELATIVEPATHHERE'	# TODO: Create function to get relative path of file
				info['CheckAlg'] = 'SHA1'
				cur.execute("""INSERT INTO package_files (file_name, file_type, file_copyright_text, 
					artifact_of_project_name, artifact_of_project_homepage, artifact_of_project_url,
					license_concluded, license_info_in_file, file_checksum, file_checksum_algorithm, relative_path, created_at)
					VALUES (""" + str(info['FileName']) + """, """ + str(info['FileType']) + """, """ + str(info['FileCopyrightText']) + """, """
						+ str(info['Artifact']) + """, """ + str(info['Artifact']) + """, """ + str(info['Artifact']) + """, """
						+ str(info['LicenseConcluded']) + """, """ + str(info['LicenseInfoInFile']) + """, """ + str(info['Checksum']) + """, """
						+ str(info['CheckAlg']) + """, """ + str(info['RelativePath']) + """,""" + time.strftime('%Y-%m-%d %H:%M:%S') + ")""")

				# TODO: insert file associations to doc_file_package_associations table
				cur.execute("""INSERT INTO doc_file_package_associations (spdx_doc_id, package_id, package_file_id, created_at, updated_at)
					VALUES (""" + str() + """, """ + str() + """, """
					+ str() + """, """ + str() + """, """ + str() + """, """
					+ str() + """, """ + str()""")""")
				
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
			with open(self.info['outfile'], 'w') as f:
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
		if os.path.exists(self.info['tar_file']):
		    package_checksum = self._hash_file(self.info['tar_file'] )
		else:
		    package_checksum = DEFAULT

		## document level information
		head.append("SPDXVersion: " + self.info['spdx_version'])
		head.append("DataLicense: " + self.info['data_license'])
		head.append("DocumentComment: <text>SPDX for "
		    + self.info['pn'] + " version " + self.info['pv'] + "</text>")
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
		head.append("PackageName: " + self.info['pn'])
		head.append("PackageVersion: " + self.info['pv'])
		head.append("PackageDownloadLocation: " + DEFAULT)
		head.append("PackageSummary: <text></text>")
		head.append("PackageFileName: " + os.path.basename(self.info['tar_file']))
		head.append("PackageSupplier: Person:" + DEFAULT)
		head.append("PackageOriginator: Person:" + DEFAULT)
		head.append("PackageChecksum: SHA1: " + package_checksum)
		head.append("PackageVerificationCode: " + spdx_verification_code)
		head.append("PackageDescription: <text>" + self.info['pn']
		    + " version " + self.info['pv'] + "</text>")
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


		
def run_do_spdx():
	from argparse import ArgumentParser
	import ConfigParser
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
	configParser = ConfigParser.ConfigParser()
	configParser.read(info['config_path'])
# 	(info['config_path'])

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

	info['fossology_server'] = configParser.get('FOSSology', 'server')
	info['fossology_flags'] = configParser.get('FOSSology', 'flags')

	# Get DoSpdx object with supplied parameters
	mDoSpdx = DoSpdx(info)
	# Run do_spdx process on that object
	completed = mDoSpdx.do_spdx()
	# Output should be for the supplied outfile, or to stdout if not supplied.
	
# Only execute run_do_spdx if the module was called from command line
if __name__ is '__main__':
	run_do_spdx()