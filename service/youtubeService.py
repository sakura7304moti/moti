import sys
sys.path.append('../utils')
sys.path.append('../model')
from youtube import youtube

def download_mp3(url):
    youtube.download_mp3(url)
    
def download_mp4(url):
    youtube.download_mp4(url)