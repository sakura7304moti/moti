import os
import shutil
import pandas as pd
import glob
import jaconv
from tqdm import tqdm
import datetime

#キャラクターの名前のリスト
df=pd.read_csv('ssbu.csv')
char_list=df['0'].to_list()

#保存先のフォルダを取得
df=pd.read_csv('ssbu_dict.csv')
tag_key_list=df['key'].to_list()
tag_val_list=df['val'].to_list()

#パスのリスト
path_list=glob.glob(r'G:\素材\スマブラの動画\*\*切り抜き\*\*')


def get_movie_path(path):
    #名前をカタカナに変換
    base_tag=os.path.basename(path).split('_')[0].split('_')[0].split('.')[0]
    kana_tag=jaconv.hira2kata(base_tag)
    
    #キャラ名一致しているかどうか
    if kana_tag in char_list:
        save_tag_name=char_list[char_list.index(kana_tag)]
    else:
        #自前で作成した名前はある？
        if base_tag in tag_key_list:
            key_index=tag_key_list.index(base_tag)
            save_tag_name=tag_val_list[key_index]
        else:
            save_tag_name='その他'
    date=path.split('\\')[-2].replace('_','')
    save_path=os.path.join(r'G:\素材\スマブラの動画\キャラクター別',save_tag_name,os.path.basename(path)).replace('.mp4','_'+date+'.mp4')
    return save_path

def split_path(path):
    base=os.path.basename(path).split('_')[0].split('_')[0]
    file_name=os.path.basename(path)
    ls=base.split('・')
    date=path.split('\\')[-2].replace('_','')
    
    path_list=[]
    for name in ls:
        res_path=get_movie_path(path.replace(base,name))
        #-------------------------------------------------
        sub_file_name=os.path.basename(res_path).replace(name,base).replace('.mp4','_'+date+'.mp4')
        sub_dir_name=os.path.dirname(res_path)
        result_path=os.path.join(sub_dir_name,sub_file_name)
        #-------------------------------------------------
        path_list.append(result_path)
    return path_list

def file_copy(path,copy_to):
    if not os.path.exists(copy_to):
        if not os.path.exists(os.path.dirname(copy_to)):
            os.makedirs(os.path.dirname(copy_to))
        shutil.copyfile(path,copy_to)
        drive_copy(path,copy_to)
        
def drive_copy(path,copy_to):
    today = datetime.date.today()
    date = today.strftime('%Y%m%d')
    char = copy_to.split('\\')[-2]
    file_name = os.path.basename(copy_to)
    
    drive_copy_dir = os.path.join(r'G:\素材\スマブラの動画_移動用',date,'キャラ別',char)
    if not os.path.exists(drive_copy_dir):
        os.makedirs(drive_copy_dir)
    cp_to = os.path.join(drive_copy_dir,file_name)
    if not os.path.exists(cp_to):
        shutil.copyfile(path,cp_to)
    
        
        
def main():
    for path in tqdm(path_list):
        if '・' in os.path.basename(path):
            res=split_path(path)
            for r in res:
                file_copy(path,r)
        else:
            changed_path=get_movie_path(path)
            file_copy(path,changed_path)
main()