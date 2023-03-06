#import
import os
import cv2
import glob
import shutil
from tqdm import tqdm
import time
from contextlib import redirect_stdout
import re

import sys
sys.path.append('../EasyOCR')

from easyocr import easyocr

#property
reader = easyocr.Reader(['en'])
save_basedir = r'G:\素材\スマブラの動画_未クリップ_キャラ名'

#function
#動画のパスを指定してndarrayを返す
def get_image(video_path):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 60)
    if not cap.isOpened():
        return
    ret, frame = cap.read()
    return frame

#1Pと2Pの画像を切り出す
def crop_image(image):
    left_image = image[670:685,350:475]
    right_image = image[670:685,840:968]
    result = {
        'left':left_image,
        'right':right_image
    }
    return result

#OCRにかける
reader = easyocr.Reader(['en'])
def ocr(image):
    result = reader.readtext(image)
    if len(result) == 0:
        return 'notFoundText'
    if len(result[0]) < 2:
        return 'notFoundText'
    return result[0][1].strip().title()

#すでに作成していたらTrue
def save_check(path):
    sub_date = os.path.basename(path).split('-')[0]
    find_result = [c for c in movie_list if sub_date in os.path.basename(c).split('-')[0]]
    saved = True if len(find_result) != 0 else False
    return saved

#動画のパスのリストを取得
def get_movie_list():
    #動画素材すべて
    video_path_list = glob.glob(r'G:\素材\スマブラの動画\*\*\*\*.mp4')
    video_path_list = [c for c in video_path_list if '切り抜き' not in c]
    video_path_list = [c for c in video_path_list if c.split('\\')[-4].isdecimal()]
    
    #作成済みの動画
    maked_list = glob.glob(r'G:\素材\スマブラの動画_未クリップ_キャラ名\*\*\*\*.mp4')
    
    #これから作成するリストを作成
    movie_list = []
    for path in video_path_list:
        number = os.path.basename(path).split('.')[0].split('-')[0]
        check_list = [path for path in maked_list if number in path]
        if len(check_list) == 0:
            movie_list.append(path)
    return movie_list

#保存先を取得
def get_path(path,right,left):
    date = path.split('\\')[-4:-1]
    save_dir = os.path.join(save_basedir,date[0],date[1],date[2])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    sub_date = os.path.basename(path).split('-')[0]
    file_name = left + '-' + right + '_' + sub_date 
    file_name = (re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '', file_name)) + '.mp4'
    save_path = os.path.join(save_dir,file_name)
    return save_path


#1ファイル単位でファイルコピーまでの一連の流れ
def rename_movie(path):
    #動画から画像の切り出し
    image = get_image(path)
    
    #画像クロップ
    result = crop_image(image)
    right_image = result['right']
    left_image = result['left']
    
    #文字をOCRで取得
    right_name = ocr(right_image)
    left_name = ocr(left_image)
    
    #保存先を取得
    save_path = get_path(path,right_name,left_name)
    
    #ファイルコピーをする
    if not os.path.exists(save_path):
        shutil.copyfile(path,save_path)
        
def main():
    movie_list = get_movie_list()
    for path in tqdm(movie_list):
        with redirect_stdout(open(os.devnull, 'w')):
            rename_movie(path)