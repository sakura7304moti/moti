import sys
sys.path.append('../utils')
sys.path.append('../model')
from pydrive import pydrive

def copy(pid,dir_name,file_path_list):
    pydrive.copy((pid,dir_name,file_path_list))