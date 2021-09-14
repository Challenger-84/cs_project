import dropbox

dropbox_access_token = "upKK1SR_CWcAAAAAAAAAAT68jYjGN_cZUkqpBAN4YMug1A5e3qsMZsa8ykikE-2Y"

client = dropbox.Dropbox(dropbox_access_token)

def upload_file(file):
    dropbox_path = '/' + file
    client.files_upload(open(file, 'rb').read(), dropbox_path)
    return file

def get_file(path):
    with open('static/cache/' + path, "wb") as f:
        metadata, result = client.files_download(path='/'+ path)
        f.write(result.content)
    
    return 'cache/' + path

