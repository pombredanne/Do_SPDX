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
# READ THE README BEFORE USING
#
# Licensing information for Do_SPDX project can be found under
# /documentation/license/LICENSE.txt
'''
Created on Apr 28, 2014

@see: www.spdx.org
@license: Apache License v2.0
@author: Corbin Haughawout
'''
import logging, datetime
from spdx.entity.spdx import SPDX
from spdx.entity.package import Package
from spdx.entity.pfile import PackageFile

LOG_CONFIG_PATH = """./do_spdx_log.cfg"""
CONFIG_PATH = """./do_spdx.cfg"""
DO_SPDX_TEMP_DIR = """/tmp/do_spdx/"""

quiet = None
force = None

logging.config.fileConfig(LOG_CONFIG_PATH)
logger = logging.getLogger()    # Root logger
package_hash = None

def do_spdx(source, author, spdx_version, 
            database_user, database_name, database_host, database_port, 
            database_pass, scanner_command, scanner_flag):
    '''
    The single entry point for the DoSpdx process.
    TODO: Add details on expectations of the process and user input,
    how it validates that input, and what it will output.
    '''
    import os, sys, tarfile
    logger.debug('In Do_SPDX()...')
    package_hash = hash_file(source)
    try:
        package = package_in_database(package_hash)
    except Exception as e:
        logger.error(e.message)
        raise
    if package is not None:
        logger.info('Package found in database')
        if force:
            logger.info('Forcing re-scan of package')
        else:
            if quiet:
                logger.info('Exiting without output')
                sys.exit(0) # Exited quietly
            else:
                logger.info('Creating output then terminating')
                try:
                    package.package_files = get_associated_files(package.package_id)
                    spdx_doc = get_package_spdx(package.package_id)
                    header = create_header(source, package, spdx_doc)
                    manifest = create_manifest(header, package.package_files)
                    print manifest
                except Exception as e:
                    logger.error(e.message)
                    raise
                sys.exit(0)
    
    if not os.path.exists(DO_SPDX_TEMP_DIR):
        os.makedirs(DO_SPDX_TEMP_DIR, 0777)
        
    unpacked = None
    
    with tarfile.open(package, 'r:gz') as tar:
        tar.extractall(DO_SPDX_TEMP_DIR)
        
def create_manifest(header, package_files):
    if not quiet:
        manifest = header.join("\n")
        for package_file in package_files:
            for member in package_file.__dict__:
                manifest.join(str(member)).join("\n")
        return manifest
    return None
            
            
            
#     if not quiet:
#         # Construct manifest
#         to_file = header + '\n'
#         for chksum, block in files.iteritems():
#             for key, value in block.iteritems():
#                 to_file += key + ": " + value
#                 to_file += '\n'
#             
#             to_file += '\n'


def create_header(source, package, spdx):
    import os
    head = []
    DEFAULT = 'NOASSERTION'
    
    # document level information
    head.append("SPDXVersion: " + spdx.spdx_version)
    head.append("DataLicense: " + spdx.data_license)
    head.append("DocumentComment: <text>SPDX for %s version %s</text>" % 
                (package.package_name, package.package_version))
    head.append("")
    
    # creator information
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    head.append('## Creation Information')
    head.append("Creator: %s" % DEFAULT)
    head.append("Created: %s" % now)
    head.append("CreatorComment: <text>UNO</text>")
    head.append("")
    
    head.append("## Package Information")
    head.append("PackageName: %s" % package.package_name)
    head.append("PackageVersion: %s" % package.package_version)
    head.append("PackageDownloadLocation: %s" % package.package_download_location)
    head.append("PackageSummary: <text>%s</text>" % package.package_summary)
    head.append("PackageFileName: %s" % os.path.basename(source))
    head.append("PackageSupplier: Person:%s" % package.package_supplier)
    head.append("PackageOriginator: Person:%s" % package.package_originator)
    head.append("PackageChecksum: SHA1: %s" % package.package_checksum)
    head.append("PackageVerificationCode: %s" % package.package_verification_code)
    head.append("PackageDescription: <text>%s version %s</text>" % (package.package_name, package.package_version))
    head.append("")
    head.append("PackageCopyrightText: <text>%s</text>" % package.package_copyright_text)
    head.append("")
    head.append("PackageLicenseDeclared: %s" % package.package_license_declared)
    head.append("PackageLicenseConcluded: %s" % package.package_license_concluded)
    head.append("PackageLicenseInfoFromFiles: %s" % package.package_license_info_from_files)
    head.append("")
    
    ## header for file level
    head.append("## File Information")
    head.append("")
    
    return "\n".join(head)
    
    
    
    
    
    
def get_package_spdx(package_id):
    '''
    @raise Exception: Raises an Exception if database query fails.
    '''
    import MySQLdb as mysql
    
    with mysql.connect(user=database_user, password=database_pass,
                        host=database_host, database=database_name) as con:
        cur = con.cursor()
        sql = "SELECT * FROM spdx_docs LEFT JOIN doc_file_package_associations on spdx_docs.id = doc_file_package_associations spdx_doc_id"
        cur.execute(sql)
        rows = cur.fetchall()
        spdx_docs = list()
        if rows is not None:
            for row in rows:
                spdx_doc = SPDX(row[0], row[1], row[2], row[3], row[4],
                                 row[5], row[6], row[7], row[8], row[9])
                spdx_docs.append(spdx_doc)
            return tuple(spdx_docs)
        return None

def get_associated_files(package_id):
    '''
    @raise Exception: Raises an Exception if database query fails.
    '''
    import MySQLdb as mysql
    
    with mysql.connect(user=database_user, password=database_pass, 
                        host=database_host, database=database_name) as con:
        cur = con.cursor()
        sql = "SELECT * FROM package_files LEFT JOIN doc_file_package_associations on package_files.id = b.package_file_id"
        cur.execute(sql)
        rows = cur.fetchall()
        
        package_files = list()
        if rows is not None:
            for row in rows:
                package_file = PackageFile(row[0], row[1], row[2], row[3],
                                           row[4], row[5], row[6], row[7],
                                           row[8], row[9], row[10], row[11],
                                           row[12], row[13], row[14], row[15],
                                           row[16], row[17], row[18])
                package_files.append(package_file)
                
                
            return tuple(package_files)
        return None

def insert_new_package(package, package_files):
    '''
    @raise Exception: Raises an Exception if Insertion into database fails.
    '''
    import MySQLdb as mysql
    
    with mysql.connect(user=database_user, password=database_pass, 
                       host=database_host, database=database_name) as con:
        cur = con.cursor()
        sql = "INSERT INTO package_files "
        try:
            cur.execute(sql)
            cur.commit()
        except:
            cur.rollback()
            raise

def package_in_database(package_checksum):
    '''
    @raise Exception: If the insert fails, raises a new exception
    '''
    import MySQLdb as mysql
    with mysql.connect(user=database_user, password=database_pass, 
                       host=database_host, database=database_name) as con:
        cur = con.cursor()
        sql = "SELECT * from packages WHERE package_checksum == " + package_checksum
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7], row[8], row[9], row[10], row[11],
                          row[12], row[13], row[14], row[15], row[16], row[17],
                          row[18], row[19], row[20], row[21], row[22])
            return package
        else:
            return None
    
    
def hash_file(path):
    '''
    @raise Exception: Raises a new exception if unable to open file.
    '''
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
            database_pass):
    import os, tarfile
    import MySQLdb as mysql
    logger.debug('Testing package...')
    if not os.path.exists(package):
        raise ValueError('Invalid path to package')
    
    if not tarfile.is_tarfile(package):
        raise ValueError('Package provided is not a tarfile.')
    logger.debug('Test successful.')
    
    logger.debug("Testing database...")
    MySQLExceptions = list()    # Used to get a list of tables missing for logging and error handling
    
    with mysql.connect(user=database_user, password=database_pass, 
            host=database_host, database=database_name) as con:
        logger.debug('Connection established @%s:%s for user %s' % (con.host, con.port, con.user))
        cur = con.cursor()
        sql_commands = list()
        sql_commands.append("SHOW TABLES LIKE 'spdx_docs'")
        sql_commands.append("SHOW TABLES LIKE 'packages'")
        sql_commands.append("SHOW TABLES LIKE 'package_files'")
        sql_commands.append("SHOW TABLES LIKE 'licenses'")
        sql_commands.append("SHOW TABLES LIKE 'doc_license_associations'")
        sql_commands.append("SHOW TABLES LIKE 'licensing'")
        sql_commands.append("SHOW TABLES LIKE 'doc_file_package_associations'")
        sql_commands.append("SHOW TABLES LIKE 'creators'")
        sql_commands.append("SHOW TABLES LIKE 'reviewers'")
        sql_commands.append("SHOW TABLES LIKE 'spdx_docs'")
        sql_commands.append("SHOW TABLES LIKE 'products'")
        sql_commands.append("SHOW TABLES LIKE 'product_software'")
        sql_commands.append("SHOW TABLES LIKE 'software'")
        try:
            for sql in sql_commands:
                logger.debug('Testing: %s' % sql)
                cur.execute(sql)
                if not cur.fetchone():
                    MySQLExceptions.append(mysql.MySQLError("Table does not exist for query: %s\n" % sql))
        except:
            raise
        
        if MySQLExceptions:
            MySQLExceptions = tuple(MySQLExceptions)
            logger.debug('Database test failed: %s' % MySQLExceptions)
            raise mysql.MySQLError("Invalid Database: %s" % MySQLExceptions)
        
    logger.debug("Test successful.")
    logger.debug("All tests successful.")
        
        

if __name__ == '__main__':
    
    from argparse import ArgumentParser
    import ConfigParser, sys, time
    
    
    start = time.clock()
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
    
    logger.debug('Finished argument parsing. package = %s; quiet = %s; force = %s' % (package, quiet, force))
    
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
    logger.debug('Finished configuration parsing. package = %s; author = ' + author + 
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
    end = time.clock()
    logger.info('Finished operations @%s in %s' % (datetime.datetime.now(), end-start)



# Factory for uncompressing a file
# Implement later 
#
# class CompressedFile (object):
#     magic = None
#     file_type = None
#     mime_type = None
#     proper_extension = None
# 
#     def __init__(self, f):
#         # f is an open file or file like object
#         self.f = f
#         self.accessor = self.open()
# 
#     @classmethod
#     def is_magic(self, data):
#         return data.startswith(self.magic)
# 
#     def open(self):
#         return None
# 
# import zipfile
# 
# class ZIPFile (CompressedFile):
#     magic = '\x50\x4b\x03\x04'
#     file_type = 'zip'
#     mime_type = 'compressed/zip'
# 
#     def open(self):
#         return zipfile.ZipFile(self.f)
# 
# import bz2
# 
# class BZ2File (CompressedFile):
#     magic = '\x42\x5a\x68'
#     file_type = 'bz2'
#     mime_type = 'compressed/bz2'
# 
#     def open(self):
#         return bz2.BZ2File(self.f)
# 
# import gzip
# 
# class GZFile (CompressedFile):
#     magic = '\x1f\x8b\x08'
#     file_type = 'gz'
#     mime_type = 'compressed/gz'
# 
#     def open(self):
#         return gzip.GzipFile(self.f)
# 
# 
# # factory function to create a suitable instance for accessing files
# def get_compressed_file(filename):
#     with file(filename, 'rb') as f:
#         start_of_file = f.read(1024)
#         f.seek(0)
#         for cls in (ZIPFile, BZ2File, GZFile):
#             if cls.is_magic(start_of_file):
#                 return cls(f)
# 
#         return None
# 
# filename='test.zip'
# cf = get_compressed_file(filename)
# if cf is not None:
#     print filename, 'is a', cf.mime_type, 'file'
#     print cf.accessor