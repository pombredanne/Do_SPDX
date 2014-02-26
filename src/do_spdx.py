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

class DoSpdx():
	def __init__(self, workdir='', sourcedir='', spdx_version='', data_license='', outfile, spdx_temp_dir='', tar_file):
		import os
		self.info = {}
		self.info['workdir'] = workdir
		self.info['sourcedir'] = sourcedir
		self.info['spdx_version'] = spdx_version
		self.info['data_license'] = data_license
		self.info['outfile'] = outfile
		self.info['spdx_temp_dir'] = spdx_temp_dir
		self.info['tar_file'] = tar_file

	def do_spdx(self, package, dest=''):
		import os, sys, json

run_do_spdx()
		
def run_do_spdx():
	import argparse
	parser = argparse.ArgumentParser(description='Generate spdx documents for a given tarfile')

	myDoSpdx = DoSpdx()
	myDoSpdx.do_spdx()

