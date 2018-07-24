import datetime
import sys
import json


from .driver import s3
from os import path, walk


class BuildPath():

    def __init__(self, s3):
        self.s3 = s3

    def parse_file_location(self, base_path, file_path):
        path_part = ''

        for item in file_path:
            if type(item) is str:
                # print('Parsing String')
                path_part = path.join(path_part, item)
            elif item['type'] == 'file':
                # print('Parsing File')
                try:
                    with open(path.join(base_path, item['path'])) as text:
                        path_part = path.join(path_part, text.read().lstrip().rstrip())
                except FileNotFoundError as error:
                    raise RuntimeError('Not Found:' + path.join(base_path, item['path'])) from error
            elif item['type'] == 's3':
                # print('Parsing s3')
                path_part = path.join(path_part, self.s3.s3_download(item['bucket'], item['key'], {}))
            # print(json.dumps(item, indent=2))

        return path_part


class GetRemoteObjectPaths():

    def __init__(self):
        self.s3 = None

    def set_s3_client(self, s3):
        self.s3 = s3

    def get_s3_downloads(self, bucket, filter):
        if self.s3 is not None:
            return self.s3.s3_search_with_prefix(bucket, filter)
        else:
            return []

def get_upload_targets(payload):
    return [{'path': path.join(root,file), 'filename':str(path.join(root,file)).replace('./','').replace(str(payload) + '/','')} for root,dir,files in walk(payload) for file in files]
