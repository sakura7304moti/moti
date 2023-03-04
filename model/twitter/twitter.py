#Import--------------------------------------------------
import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import time
import os
import urllib
import datetime
import yaml
import sys

sys.path.append('../../utils')
import utilDatetime
import utilFile
#Prepare--------------------------------------------------
yaml_path = '../../option/output.yaml'
with open(yaml_path) as file:
    yml = yaml.safe_load(file)
    
holo_image_output = yml['twitter']['holo']['image']
holo_csv_output = yml['twitter']['holo']['csv']
base_image_output = yml['twitter']['base']['image']
base_csv_output = yml['twitter']['base']['csv']

today = datetime.datetime.today()
today_text = utilDatetime.today_yyyymmddhhmmss()

holo_list = '../../option/HoloFanArt.csv'
df=pd.read_csv(holo_list, index_col=0)
word_list=df['FanArt'].tolist()

#Sub Funtion--------------------------------------------------
#ツイートを取得
def get_tweets(query):
    print('get tweets...')
    scraper = sntwitter.TwitterSearchScraper(query)
    tweets = []
    for index,tweet in enumerate(scraper.get_items()):
        images = []
        #スパム対策で高評価4以上のみ取得
        if tweet.likeCount > 4:
            try:
                for media in tweet.media:
                    images.append(media.fullUrl)

                data = [
                    tweet.url,
                    tweet.date,
                    images
                ]
                tweets.append(data)
            except:
                pass
        rep_date = tweet.date.replace(tzinfo=None)
        #ツイートと今日の日付が2週間以上の差があれば終了
        if (today - rep_date).days >= 14:
            break
        if(len(tweets) % 100 == 0 and len(tweets) > 0):
            print(' ＊'+str((today - rep_date).days), end="")
        #1000枚を上限(時間がかかるため)
        if(len(tweets) > 1000):
            break
    
    #データフレームにして保存する
    tweet_df = pd.DataFrame(
        tweets,columns = ["url","date","images"]
    )
    return tweet_df

#ツイートのデータフレームを保存する
def save_csv(tweet_df,mode,query):
    if mode == 'base':
        csv_path = os.path.join(base_csv_output,query,query+"_"+today_text+'.csv')
    if mode == 'holo':
        csv_path = os.path.join(holo_csv_output,query,query+"_"+today_text+'.csv')
    utilFile.make_folder(os.path.dirname(csv_path))
    tweet_df.to_csv(csv_path)
    return csv_path

#URLを指定して画像を保存する
def image_download(url,save_path):
    if not os.path.exists(save_path):
        response = urllib.request.urlopen(url)
        if response.status == 200:
            try:
                with open(save_path, "wb") as f:
                    f.write(response.read())
                    time.sleep(0.5)
            except:
                pass
                
#保存先を取得
def get_save_path(url,mode,query):
    file_name = url.split('/')[-1].split('?')[0]+'.jpg'
    if mode == 'base':
        save_path = os.path.join(base_image_output,query,file_name)
    if mode == 'holo':
        save_path = os.path.join(holo_image_output,query,file_name)
    folder = os.path.dirname(save_path)
    utilFile.make_folder(folder)
    return save_path

#Main Function--------------------------------------------------
def sub_download(query,mode):
    tweet_df = get_tweets(query)
    csv_path = save_csv(tweet_df,mode,query)
    for images in tqdm(tweet_df['images']):
        for url in images:
            save_path = get_save_path(url,mode,query)
            image_download(url,save_path)
            
def base_download(query):
    mode = 'base'
    sub_download(query,mode)
            
def holo_download():
    for query in tqdm(word_list):
        mode = 'holo'
        sub_download(query,mode)