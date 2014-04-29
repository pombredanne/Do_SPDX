'''
Created on Apr 28, 2014

@see: www.spdx.org
@author: Corbin Haughawout
'''
import logging

logger = logging.getLogger()

class SPDX(object):
    '''
    @summary: The SPDX class represents an SPDX document, a manifest of licensing information for a software package.
    @author: Corbin Haughawout
    '''
    spdx_id = None
    spdx_version = None
    data_license = None
    upload_file_name = None
    upload_content_type = None
    upload_file_size = None
    upload_updated_at = None
    document_comment = None
    created_at = None
    updated_at = None
    

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
        