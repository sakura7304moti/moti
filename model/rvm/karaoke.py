#--------------------＜Import＞--------------------
import torch
import sys
import os
import glob
import pyautogui
import cv2
import time
from tqdm import tqdm
import shutil
#動画編集ライブラリ
import ffmpeg 
from moviepy.editor import *
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
#RVM
sys.path.append('../../repository/RobustVideoMatting')
sys.path.append('../../repository/RobustVideoMatting.model')
from inference import convert_video
from model import MattingNetwork
#--------------------＜RVMClass＞--------------------
class RVM():
    #--------------------＜Constructor＞--------------------
    def __init__(self):
        self.model = MattingNetwork('resnet50').eval().cuda()  # or "resnet50"
        self.model.load_state_dict(torch.load('rvm_resnet50.pth'))
        
        #まだ作成してない動画のパス
        no_make_path_list=glob.glob('G:/素材/カラオケ動画/**/*.mp4')
        no_make_path_list=list(map(lambda x:x.replace('G:/素材/カラオケ動画\\',''),no_make_path_list))

        #作成した動画のパス
        ok_make_path_list=glob.glob('G:/素材/GB素材/**/*.mp4')
        ok_make_path_list=[path for path in ok_make_path_list if not '音無し' in path]
        ok_make_path_list=list(map(lambda x:x.replace('G:/素材/GB素材\\',''),ok_make_path_list))
        print('現在の進捗：',len(ok_make_path_list),'/',len(no_make_path_list))

        #作成するべき日付とファイル名
        self.make_list=[path for path in no_make_path_list if not path in ok_make_path_list]

        


    #--------------------＜Make Green Back＞--------------------
    def make(self,video_path,save_path):
        base_mp4_path='./音無しmp4/result.mp4'
        base_mp3_path="./mp3/result.mp3"
        fps_mp4_path='./音無しmp4/fps_result.mp4'
        """
        if os.path.exists(base_mp4_path):
            os.remove(base_mp4_path)
        if os.path.exists(base_mp3_path):
            os.remove(base_mp3_path)
        if os.path.exists(fps_mp4_path):
            os.remove(fps_mp4_path)
        """
        
            
        print('1.元のFPSを調節する')
        input = ffmpeg.input(video_path) 
        output = ffmpeg.output(input,fps_mp4_path,r=30) 
        ffmpeg.run(output, overwrite_output=True, quiet=True)
        
        #GB作成
        print('2．音無しのGBを作成する')
        convert_video(
        self.model,                           # The model, can be on any device (cpu or cuda).
        input_source=fps_mp4_path,        # A video file or an image sequence directory.
        output_type='video',             # Choose "video" or "png_sequence"
        output_composition=base_mp4_path,    # File path if video; directory path if png sequence.
        output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
        downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
        seq_chunk=1,                    # Process n frames at once for better parallelism.
        )
        
            
        #mp4➡mp3
        
        print('3．素材のmp4をmp3に変換する')
        fps=cv2.VideoCapture(fps_mp4_path).get(cv2.CAP_PROP_FPS)
        stream = ffmpeg.input(fps_mp4_path) 
        stream = ffmpeg.output(stream,base_mp3_path,r=30) 
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        #mp4 fps check
        
        
        
        #変換した音声と動画を合成
        if os.path.exists(base_mp3_path):
            print('4．mp4と音無しGBを合成させる')
            video_input=ffmpeg.input(base_mp4_path)
            audio_input=ffmpeg.input(base_mp3_path)
            stream=ffmpeg.output(video_input,audio_input,save_path,r=30) 
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
        
        
        print('完成！！')
    #--------------------＜Main＞--------------------
    def __call__(self):
        for path in tqdm(self.make_list):
            #最終的に作成する動画の元のパスと出力先のパスを出す
            self.video_path='G:/素材/カラオケ動画\\'+path
            self.save_path='G:/素材/GB素材\\'+path
            if not os.path.exists(os.path.dirname(self.save_path)):
                os.makedirs(os.path.dirname(self.save_path))
            print('\n【今回作成する動画のパス】')
            print(self.video_path)
            print('\n【出力先】')
            print(self.save_path)
            self.make(self.video_path,self.save_path)
#--------------------＜Instance Create＞--------------------
#rvm=RVM()
#print('\n実行準備完了')
#rvm()