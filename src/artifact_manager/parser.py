import datetime

from os import path, listdir

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
    return [ {'path' : path.join(base_path, f), 'filename': f} for f in listdir(base_path) if path.isfile(path.join(base_path, f))]
