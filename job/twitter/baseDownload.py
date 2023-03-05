import sys
sys.path.append('../../utils')
sys.path.append('../../model')
sys.path.append('../../service')

from twitterService import *

query = input('検索ワード貼り付けてね\n')
base_download(query)