import sys
sys.path.append('../../utils')
sys.path.append('../../model')
sys.path.append('../../service')

from youtubeService import *

url = input('URL貼り付けてね\n')
download_mp3(url)