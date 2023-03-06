from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.file import Storage
import os
import glob
from tqdm.notebook import tqdm

def auth_gd():
    gauth = GoogleAuth(settings_file=f"F:/Project/moti/option/settings.yaml")
    gauth.credentials = Storage(f"F:/Project/moti/option/credentials.json").get()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive


# ディレクトリがGoogle Drive上に存在するかどうかをチェックし、
# 存在しなければ作成、すでに存在すれば既存のフォルダを返す
def create_dir(pid, fname, drive=None):
    if drive == None:
        drive = auth_gd()

    ret = check_files(pid, fname, drive)
    if ret == False:
        folder = drive.CreateFile({'title': fname,
                                 'mimeType': 'application/vnd.google-apps.folder'})
        folder['parents']= [{'id': pid}]
        folder.Upload()
    else:
        folder = ret
        print(folder['title']+" exists")

    return folder

#同じ名前のファイルがGoogle Drive上に存在するかチェックし、
#存在しなければアップロード、存在すれば既存のファイルを返す
def upload_file(pid, fname, drive=None):
    if drive == None:
        drive = auth_gd()

    ret = check_files(pid, fname, drive)
    if ret == False:
        gf = drive.CreateFile()
        gf['parents']= [{'id': pid}]
        gf.SetContentFile(fname)
        gf['title'] = os.path.basename(fname)
        gf.Upload()
    else:
        gf = ret
        print(gf['title']+" exists")

    return gf

#Google Drive上にその名前のファイル/フォルダがあるかチェック、なければFalseを、あれば既存のファイル/フォルダを返す
def check_files(pid, fname, drive=None):
    if drive == None:
        drive = auth_gd()

    query = '"{}" in parents'.format(pid)
    query += ' and title = "' + os.path.basename(fname) + '"'

    list =  drive.ListFile({'q': query}).GetList()
    if len(list)> 0:
        return list[0]
    return Falsepydri
#----------------------------------------------------------------------
def copy(pid,dir_name,file_path_list):
    drive = auth_gd()
    #copy folder id--------------------------
    copyed_id = ""
    for f in drive.ListFile({'q': '"{}" in parents'.format(pid)}).GetList():
        if f['title'] == dir_name:
            copyed_id = f['id']
    #file copy---------------------------------
    for path in tqdm(path_list):
        upload_file(copyed_id,path,drive)