# -*- coding: utf-8 -*-
import os
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# 自動ログイン開始
chro = webdriver.Chrome('./chromedriver')
chro.get("https://pairs.lv/#/login") # Facebookページ遷移〜ペアーズログインページ遷移
key = input('ログイン後、pairsのトップページが出たらyを押してください')

if key == "y":
    # 1000人に到達するまで繰り返す（足跡間隔はランダムで5〜10秒の間）
    for i in range(0, 1000):
        src= "https://pairs.lv/#/search/one/%s"%str(i)
        chro.get(src)
        print("%s人目にいいね"%str(i))
        time.sleep(random.randint(3,5))

    print("1000人に足跡を付けました")

chro.close() # セッションをクローズ