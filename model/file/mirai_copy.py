import os
import shutil
import glob
import time
from tqdm import tqdm
import datetime

def get_copy_path(path):
    copy_to_dir=r'G:\素材\スマブラの動画\未来'
    return os.path.join(copy_to_dir,os.path.basename(path))

def get_drive_path(path):
    today = datetime.date.today()
    date = today.strftime('%Y%m%d')
    drive_copy_dir = os.path.join(r'G:\素材\スマブラの動画_移動用',date,'未来')
    if not os.path.exists(drive_copy_dir):
        os.makedirs(drive_copy_dir)
    return os.path.join(drive_copy_dir,os.path.basename(path))

if __name__ == "__main__":
    C_list=glob.glob(r'G:\素材\スマブラの動画\20*\**\*未来*.mp4', recursive=True)
    C_list = [path for path in C_list if not os.path.exists(get_copy_path(path))]
    print('count:',len(C_list))

    for path in tqdm(C_list):
        #ローカルへコピー
        copy_to = get_copy_path(path)
        shutil.copyfile(path,copy_to)

        #ドライブ用に別フォルダへコピー
        drive_path = get_drive_path(path)
        shutil.copyfile(path,drive_path)

    print('OK!!!')
    time.sleep(3)

