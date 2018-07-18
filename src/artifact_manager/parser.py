import datetime
from artifact_manager.driver import s3

from os import path, walk

def build_upload_path(base_dir, input):
    upload_path=''

    if input['source']['base_path']:
        upload_path=path.join(upload_path, input['source']['base_path'])

    if input['source']['path_scheme'] == 'date':
        upload_path=path.join(upload_path, datetime.datetime.today().strftime('%Y/%m/%d'))

    if input['source']['path_scheme'] == 'version':
        data = open(path.join(base_dir, input['params']['version_file']), 'rb')
        upload_path=path.join(str(upload_path), str(data.read().decode("utf-8")))
   
    return upload_path

def get_upload_targets(base_dir, input):
    base_path = path.join(base_dir, input['params']['local_path'])
    return [{'path': path.join(root,file), 'filename':str(path.join(root,file)).replace('./','').replace(str(base_path) + '/','')} for root,dir,files in walk(base_path) for file in files]

def build_download_path(base_dir, input):
    if input['source']['path_scheme'] == 'file':
        return input['params']['path']

def get_download_targets(base_dir, input):
    return input['params']['items']

def build_path(base_dir, input, s3_session):
    new_path = ''

    if 'base_path' in input['source']:
        new_path=path.join(new_path, input['source']['base_path'])

    for path_part in input['params']['path']:
        if type(path_part) is str:
            new_path=path.join(new_path,path_part)
        if type(path_part) is dict:
            new_path=path.join(new_path,parse_dict_path(path_part, s3_session))

    return new_path

def parse_dict_path(dict_path, s3_session):
    if dict_path['type'] == 's3':
        return s3_session.s3_download(dict_path['bucket'],dict_path['key'], {}).rstrip()
