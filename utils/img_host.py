import dropbox

dropbox_access_token = "sl.A4cBU2j37MplLAoqt_6RQm6GRxKcHnaszQPQN1Lb1iFW4wpD1jAOYaK8ueiLiNcFR518XV67oP-UpaHY2xzOcSAgFCGOmUujDGtnv6JiNOJcQBj4B6TTY2vbV6gH0R1fUD5dArM"

client = dropbox.Dropbox(dropbox_access_token)

def upload_file(file):
    dropbox_path = file
    client.files_upload(open(file, 'rb').read(), dropbox_path)
    return file

