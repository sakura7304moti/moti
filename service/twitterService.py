import sys
sys.path.append('../utils')
sys.path.append('../model')
from twitter import twitter

def base_download(query):
    twitter.base_download(query)
    
def holo_download():
    twitter.holo_download()