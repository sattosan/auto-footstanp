# -*- coding: utf-8 -*-
import time
import random
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

from settings import EMAIL, PASS


def login_facebook(driver):
    login_url = 'https://pairs.lv/#/login'
    facebook_login_xpath = '//*[@id="root"]/div[1]/main/div/div[1]/button'
    login_form_email_label_xpath = '//*[@id="email_container"]/div/label'
    submit_xpath = '//*[@id="u_0_0"]'

    # ペアーズのログインページ遷移
    driver.get(login_url)
    # Facebookログインボタンをクリック
    click_element_by_xpath(facebook_login_xpath, driver)
    # Facebookログインページにフォーカス
    driver.switch_to.window(driver.window_handles[-1])
    # メールアドレスとパスワードの入力
    input_form_by_name('email', EMAIL, driver)
    input_form_by_name('pass', PASS, driver)
    # どこかクリックしないと送信ボタンが押せないので，適当に押す
    click_element_by_xpath(login_form_email_label_xpath, driver)
    # ログインボタンをクリック
    click_element_by_xpath(submit_xpath, driver)
    # ログイン後，メインページにフォーカスを戻す
    driver.switch_to.window(driver.window_handles[0])


def exec_footstanp(driver, n, layout_title):
    first_icon_xpath = '//*[@id="root"]/div[1]/main/div/div[1]/a[1]'
    next_carousel_xpath = '//*[@id="dialog-root"]/div[8]/div/div[1]/div/div[3]/div[2]/a'
    sub_next_carousel_xpath = '//*[@id="dialog-root"]/div[7]/div/div[1]/div/div[3]/div[2]/a'
    modal_button_xpath = '//*[@id="dialog-root"]/div[7]/div/div[1]/div[2]/button'

    driver.get('https://pairs.lv/search')
    # キャンペーンモダールが表示されていた場合
    if check_exists_by_xpath(modal_button_xpath, driver):
        click_element_by_xpath(modal_button_xpath, driver)
    exec_scroll(scroll_num=5, driver=driver)

    search_detail_link = get_xpath_by_layout_title(layout_title, driver)
    if not search_detail_link:
        print('No Such Layout Detail Link')
        return

    print(f"=========={n}人に足跡をつけます==========")
    click_element_by_xpath(search_detail_link, driver)
    exec_scroll(scroll_num=10, driver=driver)
    click_element_by_xpath(first_icon_xpath, driver)
    # カルーセルのリンクが定期的に変わるのでチェック
    if not check_exists_by_xpath(next_carousel_xpath, driver):
        if check_exists_by_xpath(sub_next_carousel_xpath, driver):
            next_carousel_xpath = sub_next_carousel_xpath
        else:
            print('No Such Carousel')
            return
    # n人に到達するまで繰り返す（足跡間隔はランダムで3〜4秒の間）
    for i in range(0, int(n)):
        if not check_exists_by_xpath(next_carousel_xpath, driver):
            break
        click_element_by_xpath(next_carousel_xpath, driver)
        print(f"{i}人目に足跡ぺた〜")
        time.sleep(random.randint(5, 8))
    print(f"=========={n}人に足跡をつけました==========")


def exec_scroll(scroll_num, driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(0, scroll_num):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_xpath_by_layout_title(layout_title, driver):
    for layout_num in range(0, 12):
        title_xpath = f'//*[@id="layout-{layout_num}"]/aside/div/div/h2'
        layout_detail_link_xpath = f'//*[@id="layout-{layout_num}"]/aside/div/div/a'
        if not check_exists_by_xpath(title_xpath, driver):
            continue

        title = driver.find_element_by_xpath(title_xpath).get_attribute("textContent")
        if layout_title == title:
            if not check_exists_by_xpath(layout_detail_link_xpath, driver):
                break
            return layout_detail_link_xpath

    return ''


def click_element_by_xpath(xpath, driver):
    if not check_exists_by_xpath(xpath, driver):
        print('No Such Element')
    driver.find_element_by_xpath(xpath).click()


def input_form_by_name(name, value, driver):
    if not check_exists_by_name(name, driver):
        print('No Such Element')
    driver.find_element_by_name(name).send_keys(value)


def check_exists_by_xpath(xpath, driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False
    return True


def check_exists_by_name(name, driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, name)))
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True


def exec_input(input_text, default_input="0"):
    input_str = input(input_text)
    # 入力が数字じゃなかったら
    if not input_str.isdigit():
        input_str = default_input
    else:
        # 強制的に数字を半角に変換
        input_str = unicodedata.normalize('NFKC', input_str)

    return input_str


def main(driver):
    layout_titles = [
        '新着のお相手',
        '同年代のお相手',
        '出身地が一緒のお相手',
        '職業が一緒のお相手',
        '結婚に対する意思が一緒のお相手',
        'あしあと'
    ]
    # facebookを使ってログイン
    login_facebook(driver)
    # 標準入力の実行
    footstanp_num = exec_input('何人に足跡つけますか？ 数字を入力してください > ', "100")
    for i, layout_title in enumerate(layout_titles):
        print(f'{i}: {layout_title}')
    # 標準入力の実行
    index = exec_input('どのカテゴリに対して足跡を付けますか？ 数字を入力してください > ', "0")
    # 標準入力から検索したいレイアウトタイトルを探す
    layout_title = layout_titles[int(index) if int(index) < len(layout_titles) else 0]
    print(f'「{layout_title}」から足跡を付けます')
    # 自動足跡を実行
    exec_footstanp(driver, footstanp_num, layout_title)


if __name__ == '__main__':
    try:
        # Headless Chromeブラウザに接続
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        # seleniumの動作タイムアウトを10秒間に設定
        driver.implicitly_wait(10)
        # 足跡自動プロセス実行
        main(driver)
    # 例外処理
    except ElementClickInterceptedException as ecie:
        print(f"exception!\n{ecie}")
    except TimeoutException as te:
        print(f"timeout!\n{te}")
    except KeyboardInterrupt:
        print("\napp shutdown!")
    finally:
        # 終了
        driver.close()
        driver.quit()
