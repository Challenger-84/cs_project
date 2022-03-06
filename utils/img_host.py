import os
from pathlib import Path

import dropbox


def upload_file(file):
    dropbox_access_token = os.getenv("DROPBOX_TOKEN")
    client = dropbox.Dropbox(dropbox_access_token)

    dropbox_path = "/" + file
    client.files_upload(open(file, "rb").read(), dropbox_path)
    return file


def get_file(path):
    dropbox_access_token = os.getenv("DROPBOX_TOKEN")
    client = dropbox.Dropbox(dropbox_access_token)

    # Gets stored in cache folder which will be cleared every 24 hours
    if not Path("static/cache/" + path).is_file():
        with open("static/cache/" + path, "wb") as f:
            metadata, result = client.files_download(path="/" + path)
            f.write(result.content)

    return "cache/" + path
