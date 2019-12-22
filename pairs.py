# -*- coding: utf-8 -*-
import time
import random
import os
import signal
import unicodedata
from selenium import webdriver
from settings import EMAIL, PASS

def facebookLogin(driver):
    # Facebookログインボタンをクリック
    driver.find_element_by_xpath('//*[@id="registerBtn1"]').click()
    # Facebookログインページにフォーカス
    driver.switch_to.window(driver.window_handles[-1])
    # メールアドレスとパスワードの入力
    driver.find_element_by_name("email").send_keys(EMAIL)
    driver.find_element_by_name("pass").send_keys(PASS)
    # どこかクリックしないと送信ボタンが押せないので，適当に押す
    driver.find_element_by_xpath('//*[@id="email_container"]/div/label').click()
    # ログインボタンをクリック
    driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
    # ログイン後，メインページにフォーカスを戻す
    driver.switch_to.window(driver.window_handles[0])

def execFootStanp(driver, n):
    print(f"=========={n}人に足跡をつけます==========")
    # n人に到達するまで繰り返す（足跡間隔はランダムで3〜4秒の間）
    for i in range(1, int(n)+1):
        driver.get(f"https://pairs.lv/#/search/one/{i}")
        print(f"{i}人目に足跡ぺた〜")
        time.sleep(random.randint(3,5))
    print(f"=========={n}人に足跡をつけました==========")

def main(driver):
    # ペアーズのログインページ遷移
    driver.get("https://pairs.lv/#/login")
    # facebookを使ってログイン
    facebookLogin(driver)
    n = input('何人に足跡つけますか？ 数字を入力してください > ')
    # 入力が数字じゃなかったら
    if not n.isdigit():
        # デフォルトで1000人に設定
        n = "1000"
    else:
        # 強制的に数字を半角に変換
        n = unicodedata.normalize('NFKC', n)
    # 自動足跡を実行
    execFootStanp(driver, n)

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome('./driver/chromedriver')
        # seleniumの動作タイムアウトを10秒間に設定
        driver.implicitly_wait(10)
        main(driver)
        # セッションをクローズ
        driver.close()
    # 例外処理
    except TimeoutError:
        print("\ntimeout!")
    except KeyboardInterrupt:
        print("\napp shutdown!")
    # 例外発生時プロセスを強制的にキル
    finally:
        os.kill(driver.service.process.pid,signal.SIGTERM)