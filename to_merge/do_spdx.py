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
from symbol import except_clause

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
# READ THE README BEFORE USING
#
# Licensing information for Do_SPDX project can be found under
# /documentation/license/LICENSE.txt
'''
Created on Apr 28, 2014

@license: 
@author: Corbin Haughawout
'''
import logging, datetime
from spdx.entity.spdx import spdx
from spdx.entity.package import Package
from spdx.entity.pfile import PackageFile

LOG_CONFIG_PATH = """./do_spdx_log.cfg"""
CONFIG_PATH = """./do_spdx.cfg"""
DO_SPDX_TEMP_DIR = '''/tmp/do_spdx/'''

quiet = None
force = None

logging.config.fileConfig(LOG_CONFIG_PATH)
logger = logging.getLogger()    # Root logger
package_hash = None

def do_spdx(package, author, spdx_version, 
            database_user, database_name, database_host, database_port, 
            database_pass, scanner_command, scanner_flag):
    import os, sys, tarfile
    logger.debug('In Do_SPDX()...')
    package_hash = hash_file(package)
    
    if package_in_database(package_hash):
        logger.info('Package found in database')
        if force:
            logger.info('Forcing re-scan of package')
        else:
            if quiet:
                logger.info('Exiting without output')
                sys.exit(0) # Exited quietly
            else:
                logger.info('Creating output then terminating')
                '''
                @todo:  implement using entity package
                ''' 
                
                sys.exit(0)
    
    if not os.path.exists(DO_SPDX_TEMP_DIR):
        os.makedirs(DO_SPDX_TEMP_DIR, 0777)
        
    unpacked = None
    
    open_success = False
    with tarfile.open(package, 'r:gz') as tar:
        tar.extractall(DO_SPDX_TEMP_DIR)

    package_id = get_package_id(package_hash)
    

def get_package_id(package_hash):
    pass

def package_in_database(hash):
    pass
    
def hash_file(path):
    with open(path, 'rb') as f:
        data_string = f.read()
        sha1 = hash_string(data_string)
    return sha1

def hash_string(string):
    from hashlib import sha1
    file_sha1 = sha1()
    file_sha1.update(string)
    return file_sha1.hexdigest()

def validate_parameters(package, author, spdx_version, 
            database_user, database_name, database_host, database_port, 
            database_pass, scanner_command, scanner_flag):
    import os, tarfile
    
    if not os.path.exists(package):
        raise ValueError('Invalid path to package')
    
    if not tarfile.is_tarfile(package):
        raise ValueError('Package provided is not a tarfile.')
    

if __name__ == '__main__':
    
    from argparse import ArgumentParser
    import ConfigParser, sys
    
    logger.info('Starting Do_SPDX @' + datetime.datetime.now())
    logger.debug('Begin argument parsing...')
    parser = ArgumentParser(prog="Do_SPDX", usage="./do_spdx.py FILE [OPTIONS]", 
                            description="Generate spdx documents for the provided tarfile", version="1")
    parser.add_argument('file', action='append', required=True, type=file, help='Create SPDX for this package')
    parser.add_argument('-q', '--quiet', action='append', required=False, help='Mute the output of the generated SPDX document on stdout')
    parser.add_argument('-f', '--force', action='append', required=False, help='Force the insertion of a new entry to the database for the given package')
    args = parser.parse_args() # defaults to sys.args
    
    package = args.package
    if args.quiet:
        quiet = args.quiet
    if args.force:
        force = args.force
    # END CLI
    
    logger.debug('Finished argument parsing. package = ' + package + 
                 '; quiet = ' + quiet + '; force = ' + force)
    
    logger.debug('Begin configuration parsing...')
    # Begin configuration parsing
    configParser = ConfigParser.ConfigParser()
    configParser.read(CONFIG_PATH)
    
    # General Settings
    author = configParser.get('Settings', 'author')
    spdx_version = configParser.get('Settings', 'spdx_version')
    
    # Database Settings
    database_user = configParser.get('Database', 'database_user')
    database_name = configParser.get('Database', 'database_name')
    database_host = configParser.get('Database', 'database_host')
    database_port = configParser.get('Database', 'database_port')
    database_pass = configParser.get('Database', 'database_pass')
    
    # Scanner Settings
    scanner_command = configParser.get('Scanner', 'command')
    scanner_flag = configParser.get('Scanner', 'flag')
    logger.debug('Finished configuration parsing. package = ' + package + '; author = ' + author + 
                 '; spdx_version = ' + spdx_version + '; database_user = ' + database_user + '; database_name = ' + database_name + 
                 '; database_host = ' + database_host + '; database_port = ' + database_port + '; database_pass = ' + database_pass)
    
    logger.info('Begin operations...')
    try:
        validate_parameters(package, author, spdx_version, 
                database_user, database_name, database_host, database_port, 
                database_pass, scanner_command, scanner_flag)
    except ValueError as e:
        logger.error(e.message)
        sys.exit(1) # Return 1 for invalid input
    do_spdx(package, author, spdx_version, 
            database_user, database_name, database_host, database_port, 
            database_pass, scanner_command, scanner_flag)
    logger.info('Finished operations @' + datetime.datetime.now())

class CompressedFile (object):
    magic = None
    file_type = None
    mime_type = None
    proper_extension = None

    def __init__(self, f):
        # f is an open file or file like object
        self.f = f
        self.accessor = self.open()

    @classmethod
    def is_magic(self, data):
        return data.startswith(self.magic)

    def open(self):
        return None

import zipfile

class ZIPFile (CompressedFile):
    magic = '\x50\x4b\x03\x04'
    file_type = 'zip'
    mime_type = 'compressed/zip'

    def open(self):
        return zipfile.ZipFile(self.f)

import bz2

class BZ2File (CompressedFile):
    magic = '\x42\x5a\x68'
    file_type = 'bz2'
    mime_type = 'compressed/bz2'

    def open(self):
        return bz2.BZ2File(self.f)

import gzip

class GZFile (CompressedFile):
    magic = '\x1f\x8b\x08'
    file_type = 'gz'
    mime_type = 'compressed/gz'

    def open(self):
        return gzip.GzipFile(self.f)


# factory function to create a suitable instance for accessing files
def get_compressed_file(filename):
    with file(filename, 'rb') as f:
        start_of_file = f.read(1024)
        f.seek(0)
        for cls in (ZIPFile, BZ2File, GZFile):
            if cls.is_magic(start_of_file):
                return cls(f)

        return None

filename='test.zip'
cf = get_compressed_file(filename)
if cf is not None:
    print filename, 'is a', cf.mime_type, 'file'
    print cf.accessor
    
    
    