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
class SPDX(object):
    '''
    @summary: The SPDX class represents an SPDX document, a manifest of licensing information for a software package.
    @author: Corbin Haughawout
    '''

    def __init__(self, _id, spdx_version, data_license, upload_file_name, upload_content_type,
                 upload_file_size, upload_updated_at, document_comment, created_at, updated_at):
        '''
        Initializes the spdx object
        '''
        self.spdx_id = id
        self.spdx_version = spdx_version
        self.data_license = data_license
        self.upload_file_name = upload_file_name
        self.upload_content_type = upload_content_type
        self.upload_file_size = upload_file_size
        self.upload_updated_at = upload_updated_at
        self.document_comment = document_comment
        self.created_at = created_at
        self.updated_at = updated_at
        