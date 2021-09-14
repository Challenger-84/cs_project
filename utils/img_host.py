import os
import dropbox

def upload_file(file):
    dropbox_access_token = os.getenv('DROPBOX_TOKEN')
    client = dropbox.Dropbox(dropbox_access_token)
    
    dropbox_path = '/' + file
    client.files_upload(open(file, 'rb').read(), dropbox_path)
    return file

def get_file(path):
    dropbox_access_token = os.getenv('DROPBOX_TOKEN')
    client = dropbox.Dropbox(dropbox_access_token)

    with open('static/cache/' + path, "wb") as f:
        metadata, result = client.files_download(path='/'+ path)
        f.write(result.content)
    
    return 'cache/' + path

