import sys
sys.path.append('../utils')
sys.path.append('../model')
from rvm import karaoke
from rvm import make

def make_karaoke_greenback():
    model = karaoke.RVM()
    model()
    
def greenBack(input_video,output_video):
    make.greenBack(input_video,output_video)