import subprocess
import os
import glob
import shutil

base_dir_name = 'カラオケ動画_音分離'

#作成する動画のパスのリスト取得
def get_movie_list():
    #作成する動画のパスのリスト
    video_list = glob.glob(r'G:\素材\カラオケ動画\*\*.mp4')

    #作成するべき動画のパスのリスト
    make_list = [path for path in video_list if not os.path.exists(path.replace('カラオケ動画',base_dir_name).replace('mp4','')+'\\bass.wav')]
    print('make list : ',len(make_list))
    make_list.reverse()
    return make_list

#作成した音声を保存
def copy_file(video_path):
    #作成したファイルの保存先
    base_save_dir = 'G:/素材/'+base_dir_name
    date = video_path.split('\\')[-2]
    video_name = os.path.basename(video_path).split('.')[0]

    save_dir = os.path.join(base_save_dir,date,video_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    #ファイルコピーを実行
    copy_from_list = glob.glob(r'E:\Python\demucs\separated\*\*\*.wav')
    for path in copy_from_list:
        copy_to = os.path.join(save_dir,os.path.basename(path))
        shutil.copyfile(path,copy_to)
        

#Main
path_list = get_movie_list()
for video_path in path_list:
    index = path_list.index(video_path)
    print('Index {0}/{1}'.format(str(index),str(len(path_list))))
    print('使用ファイル')
    print(video_path)
    #使用ファイルを指定場所にコピー
    shutil.copyfile(video_path,r'E:\Python\demucs\input.mp4')
    
    #音声分離実行
    subprocess.run(['conda','activate','demucs','&','demucs','input.mp4'],shell=True,text=True)
    
    #作成した音声を保存
    copy_file(video_path)
    print('OK!')
    
    #input.mp4削除
    if os.path.exists('input.mp4'):
        os.remove('input.mp4')