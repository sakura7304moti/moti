import sys
sys.path.append('../utils')
sys.path.append('../model')
from pixiv import pixiv

def basePixivDownload(target, r18, update_ignore=True):
    pixiv.basePixivDownload(target, r18, update_ignore)
    
def holoPixivDownload(r18=1):
    pixiv.holoPixivDownload(r18)