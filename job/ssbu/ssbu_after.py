import sys
sys.path.append('../../utils')
sys.path.append('../../model')
sys.path.append('../../service')

from pydriveService import copy,upload
from file import mirai_copy,ssbu_copy,ssbu_memory_copy,ultra_copy

#file copy
mirai_copy()
ssbu_copy()
ssbu_memory_copy()
ultra_copy()

#drive copy
#Ultra C
"""

import glob
import os
from tqdm import tqdm
date_list = glob.glob(r'G:\素材\スマブラの動画_移動用\*')
date = date_list[-1]
from_list = glob.glob(os.path.join(date,'ウルトラC','*.mp4'))
for path in tqdm(from_list, desc="ウルトラC"):
    upload('1V2228PudPO4G4X6sMhatw7pZnlxjBTaL',path)
    
#memory
date_list = glob.glob(r'G:\素材\スマブラの動画_移動用\*')
date = date_list[-1]
from_list = glob.glob(os.path.join(date,'思い出','*.mp4'))
for path in tqdm(from_list, desc="思い出"):
    upload('1gticLAjyl5GTwsMSbBEdvas2OrEgSSA8',path)
    
#未来
date_list = glob.glob(r'G:\素材\スマブラの動画_移動用\*')
date = date_list[-1]
from_list = glob.glob(os.path.join(date,'未来','*.mp4'))
for path in tqdm(from_list, desc="未来"):
    upload('1gticLAjyl5GTwsMSbBEdvas2OrEgSSA8',path)
    
#キャラ別
date_list = glob.glob(r'G:\素材\スマブラの動画_移動用\*')
date = date_list[-1]
char_list = glob.glob(os.path.join(date,'キャラ別','*'))
for char in tqdm(char_list,desc="キャラ"):
    char_name = os.path.basename(char)
    from_list = glob.glob(os.path.join(char,'*.mp4'))
    copy('1Yx9hZQXZjR2o_4nFsgLhrwD0VoLISynd',char_name,from_list)
    
"""