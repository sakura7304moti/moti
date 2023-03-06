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

model = MattingNetwork('resnet50').eval().cuda()  # or "resnet50"
model.load_state_dict(torch.load('rvm_resnet50.pth'))

#--------------------＜Function＞--------------------
def greenBack(input_video,output_video):
    convert_video(
        model,                           # The model, can be on any device (cpu or cuda).
        input_source=input_video,        # A video file or an image sequence directory.
        output_type='video',             # Choose "video" or "png_sequence"
        output_composition=output_video,    # File path if video; directory path if png sequence.
        output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
        downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
        seq_chunk=1,                    # Process n frames at once for better parallelism.
        )