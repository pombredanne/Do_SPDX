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

@see: www.spdx.org
@author: Corbin Haughawout
'''

class PackageFile(object):
    '''
    Represents a file in a package
    @author: Corbin Haughawout
    '''
    
    def __init__(self, file_id, file_name, file_type, file_copyright_text, 
                 artifact_of_project_name, artifact_of_project_homepage,
                 artifact_of_project_uri, license_concluded, license_info_in_file,
                 file_checksum, file_checksum_algorithm, relative_path,
                 license_comments, file_notice, file_contributor,
                 file_dependency, created_at, updated_at):
        '''
        Initializes a PackageFile object
        '''
        self.file_id = file_id
        self.file_name = file_name
        self.file_type = file_type
        self.file_copyright_text = file_copyright_text
        self.artifact_of_project_name = artifact_of_project_name
        self.artifact_of_project_homepage = artifact_of_project_homepage
        self.artifact_of_project_uri = artifact_of_project_uri
        self.license_concluded = license_concluded
        self.license_info_in_file = license_info_in_file
        self.file_checksum = file_checksum
        self.file_checksum_algorithm = file_checksum_algorithm
        self.relative_path = relative_path
        self.license_comments = license_comments
        self.file_notice = file_notice
        self.file_contributor = file_contributor
        self.file_dependency = file_dependency
        self.created_at = created_at
        self.updated_at = updated_at
        

        