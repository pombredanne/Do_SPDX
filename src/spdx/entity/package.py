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

'''
Created on Apr 28, 2014

@license: Apache License v2.0
@see: www.spdx.org
@author: Corbin Haughawout
'''

class Package(object):
    '''
    @summary: The Package class represents a software package, 
        SPDX documentation is generated from this.
    @author: Corbin Haughawout
    '''
    def __init__(self, _id=None, package_name=None, package_file_name=None, package_download_location, package_copyright_text,
                 package_version, package_description, package_summary, package_originator,
                 package_supplier, package_license_concluded, package_license_declared, package_checksum,
                 checksum_algorithm, package_home_page, package_source_info, package_license_info_from_files,
                 package_license_comments, package_verification_code, package_verification_code_excluded_file,
                 created_at, updated_at):
        '''
        Initializes the package object
        '''
        self.package_id = _id
        self.package_name = package_name
        self.package_file_name = package_file_name
        self.package_download_location = package_download_location
        self.package_copyright_text = package_copyright_text
        self.package_version = package_version
        self.package_description = package_description
        self.package_summary = package_summary
        self.package_originator = package_originator
        self.package_supplier = package_supplier
        self.package_license_concluded = package_license_concluded
        self.package_license_declared = package_license_declared
        self.package_checksum = package_checksum
        self.checksum_algorithm = checksum_algorithm
        self.package_home_page = package_home_page
        self.package_source_info= package_source_info
        self.package_license_info_from_files = package_license_info_from_files
        self.package_license_comments = package_license_comments
        self.package_verification_code = package_verification_code
        self.package_verification_code_excluded_file = package_verification_code_excluded_file
        self.created_at = created_at
        self.updated_at = updated_at    
    