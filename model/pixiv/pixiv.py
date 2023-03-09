from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from tqdm.notebook import tqdm
import yaml
import urllib
import os
import shutil
import urllib
import urllib.error
import urllib.request
import pyautogui
import re
import pyautogui
import glob
import csv
import pandas as pd
import datetime


class PixivDL:
    def setter(self, target, r18, update_ignore=True):
        self.target = target
        self.r18 = r18
        self.update_ignore = update_ignore

        if self.r18 == True:
            self.save_tag = "R18"
        else:
            self.save_tag = "Basic"
        self.pixiv_url = "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=ja&source=pc&view_type=page"

        # ログインデータ
        with open(r"E:\sakura0moti\option\pixiv\key.yaml", "r") as yf:
            dic = yaml.safe_load(yf)
            self.username = dic["user"]
            self.password = dic["pass"]
        yf.close()

        # 基準となる保存先
        self.save_base_path = r"G:\Data\Pixiv"
        self.save_dir = os.path.join(self.save_base_path, self.save_tag, self.target)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            self.update = True
        else:
            if self.update_ignore == False:
                # ファイルの更新日時
                ts = os.path.getmtime(self.save_dir)

                # datetime型に変換
                update = datetime.datetime.fromtimestamp(ts).date()

                # 今日と昨日の日付取得
                today = datetime.datetime.now().date()
                yesterday = today + datetime.timedelta(days=-1)
                # 今日か昨日？
                print(
                    "最終更新日：",
                    str(update.year) + "/" + str(update.month) + "/" + str(update.day),
                )
                if update == today or update == yesterday:
                    print("ダウンロード実行しません")
                    self.update = False
                else:
                    print("ダウンロード実行します")
                    self.update = True
            else:
                self.update = True
                print("更新日時関係なくダウンロードを実行します")
        print("画像の保存先")
        print(self.save_dir, "\n")

        # URLリストの保存先
        self.url_base_save_dir = r"G:\Data\Pixiv\URL_list"
        if not os.path.exists(self.url_base_save_dir):
            os.makedirs(self.url_base_save_dir)

        self.err = False

    def main(self, target, r18, update_ignore=True):
        # 初期設定
        self.setter(target, r18, update_ignore=True)

        # ログインする
        self.login()

        # 下までスクロールする
        self.scroll()

        # 最大ページ数分の画像のURLのリストを取得する(最大7ページ)
        self.get_all_url()

        # 取得したURLを保存する
        self.save_url_list()

        # 保存したリストをもとにダウンロードする
        image_count = self.all_download(self.save_url_list_path)
        return image_count

    def login(self):
        # chromeを開くための初期設定
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options
        )
        # -----------------------------------------------------------------------------------

        # ピクシブを開く
        self.driver.get(self.pixiv_url)
        self.driver.minimize_window()
        time.sleep(1)
        self.driver.maximize_window()
        # ログイン
        # driver.find_element(By.CLASS_NAME,'signup-form__submit--login').click()
        self.driver.find_element(
            By.XPATH, "//input[@autocomplete='username']"
        ).send_keys(self.username)
        self.driver.find_element(
            By.XPATH, "//input[@autocomplete='current-password']"
        ).send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # -----------------------------------------------------------------------------------
        # URL変更
        if self.r18 == True:
            self.replace_url = (
                "https://www.pixiv.net/tags/"
                + urllib.parse.quote(self.target)
                + "/artworks?mode=r18&s_mode=s_tag"
            )
        else:
            self.replace_url = (
                "https://www.pixiv.net/tags/"
                + urllib.parse.quote(self.target)
                + "/artworks?mode=safe&s_mode=s_tag"
            )
        self.driver.get(self.replace_url)

    def scroll(self):
        self.driver.find_element(By.TAG_NAME, "body").click()

        timeout = 3  # [seconds]

        self.timeout_start = time.time()

        while time.time() < self.timeout_start + timeout:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

    def replace_url(self, start_url):
        url_split = start_url.split("/")

        rep1 = url_split[3] + "/" + url_split[4] + "/" + url_split[5]
        start_url = start_url.replace(rep1, "img_original")

        rep2 = "_" + url_split[-1].split("_")[-1].split(".")[0]
        url = start_url.replace(rep2, "")
        return url

    # -----1ページに対するURLのリストを取得-----
    def get_img_list(self):
        img_list = []
        count_list = []
        ul_list = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/section/div[2]/ul",
        )  # UL
        li_list = ul_list.find_elements(By.TAG_NAME, "li")  # LI

        for li in li_list:

            # アートタグ
            tag = ""
            try:
                url = li.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                self.err = True
            else:
                img_list.append(url)

                # 画像枚数
                image_count = 1
                span_list = li.find_elements(By.TAG_NAME, "span")
                for span in span_list:
                    text = span.text.replace(" ", "").replace("　", "")
                    if text.isdecimal() == True:
                        image_count = str(text)
                count_list.append(image_count)

        for i in range(len(img_list)):
            url = img_list[i]
            count = int(count_list[i])
            for c in range(count):
                image_url = url.replace("p0", "p" + str(c))
                url_split = image_url.split("/")

                rep1 = url_split[3] + "/" + url_split[4] + "/" + url_split[5]
                image_url = image_url.replace(rep1, "img-original")

                rep2 = "_" + url_split[-1].split("_")[-1].split(".")[0]
                image_url = image_url.replace(rep2, "")
                if not image_url in self.img_list:
                    self.img_list.append(image_url)

    # ページ数取得
    def get_page(self):
        for e in self.driver.find_elements(By.TAG_NAME, "nav"):
            i = e.find_elements(By.TAG_NAME, "span")
        self.page = len(i)
        page = self.page
        return page

    def get_all_url(self):
        self.img_list = []
        ls = range(1, self.get_page() + 1)
        for l in tqdm(ls, desc="Image Search"):

            page_url = self.replace_url + "&p={0}".format(l)
            self.driver.get(page_url)
            self.scroll()
            self.get_img_list()
        self.driver.quit()
        print("\nダウンロードする画像数")
        print(len(self.img_list))

    def save_url_list(self):
        df = pd.DataFrame(self.img_list)
        dt_now = datetime.datetime.now()
        now = dt_now.strftime("%Y%m%d_%H%M%S")
        self.save_url_list_path = os.path.join(
            self.url_base_save_dir, self.save_tag, self.target, now + ".csv"
        )
        if not os.path.exists(os.path.dirname(self.save_url_list_path)):
            os.makedirs(os.path.dirname(self.save_url_list_path))

        print("URL_List保存先")
        print(self.save_url_list_path, "\n")
        df.to_csv(self.save_url_list_path, index=False)

    def all_download(self, path):
        self.no_save_list = []
        self.df = pd.read_csv(path)
        url_list = self.df["0"].to_list()

        image_count = 0
        for url in tqdm(url_list, desc="Image Download"):
            if url != "":
                response = requests.get(
                    url, headers={"Referer": "https://app-api.pixiv.net/"}, stream=True
                )
                save_path = os.path.join(self.save_dir, url.split("/")[-1])
                if response.status_code == requests.codes.ok:
                    if not os.path.exists(save_path):
                        with open(save_path, "wb") as f:
                            shutil.copyfileobj(response.raw, f)
                            image_count = image_count + 1
                        time.sleep(1)
                else:
                    # jpgとpng入れ替える処理作る
                    if "jpg" in url:
                        url = url.replace("jpg", "png")
                    else:
                        if "png" in url:
                            url = url.replace("png", "jpg")
                    response = requests.get(
                        url,
                        headers={"Referer": "https://app-api.pixiv.net/"},
                        stream=True,
                    )
                    save_path = os.path.join(self.save_dir, url.split("/")[-1])
                    if response.status_code == requests.codes.ok:
                        if not os.path.exists(save_path):
                            with open(save_path, "wb") as f:
                                shutil.copyfileobj(response.raw, f)
                                image_count = image_count + 1
                            time.sleep(1)
        return image_count
    
def basePixivDownload(target, r18, update_ignore=True):
    model = PixivDL(name, r18,update_ignore)
    model.main(name, r18,update_ignore)


def holoPixivDownload(r18=1):
    holo_csv_path = "../option/pixiv/HoloFullName.csv"
    df = pd.read_csv(holo_csv_path, index_col=0)
    holoNameList = df["FullName"].to_list()

    for name in tqdm(holoNameList, desc="Name Progress"):
        model = PixivDL(name, r18)
        if len(glob.glob(os.path.join(model.save_dir, "*"))) == 0:
            model.main()
