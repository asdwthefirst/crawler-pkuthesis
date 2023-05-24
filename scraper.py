import os
import re
import sys
import time
import converter
# import datetime
# import requests

from urllib.request import urlretrieve
from selenium import webdriver
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome("./chromedriver")
output_dir = './'


# 论文链接
def scrap_by_url(name, thsis_url, target_dir):
    print('start scrap %s' % name)
    # thsis_url = f"https://thesis.lib.pku.edu.cn/docinfo.action?id1={id1}&id2={id2}"
    # print(thsis_url)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(thsis_url)
    driver.refresh()

    time.sleep(2)

    # lookbut=driver.find_element_by_link_text('查看全文')
    lookbut = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/a')
    lookbut.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    time.sleep(2)

    # 获取总页数
    tpage = driver.find_element(By.CSS_SELECTOR, 'span#totalPages.toolbar-page-num')
    total_pages = int(re.sub("\D", "", tpage.get_attribute("innerText")))
    print('本论文总页数为：%d 页' % (total_pages))
    total_pages = int(total_pages)

    # 下载论文
    os.makedirs(target_dir, exist_ok=True)
    i = 0
    find_page = False

    img_urls = []
    btnnext = driver.find_element(By.CSS_SELECTOR, 'a#btnnext.toobar-btn.toobar-btn-next')
    btnpre = driver.find_element(By.CSS_SELECTOR, 'a#btnpre.toobar-btn.toobar-btn-pre')

    while i < total_pages:
        div_name = 'div#loadingBg%d.loadingbg > img' % (i)
        target_file = os.path.join(target_dir, 'img%d.jpg' % (i + 1))
        if os.path.exists(target_file):
            print(f"{target_file} already exists")
            i = i + 1
            btnnext.click()
            continue
        try:
            pics = driver.find_element(By.CSS_SELECTOR, div_name)
            img_url = pics.get_attribute('src')
            find_page = True
            img_urls.append(img_url)
        except Exception as e:
            # print('error ',e)
            find_page = False

        if find_page:
            print('找到第%d页...%s' % ((i + 1), img_url))
            i = i + 1
            btnnext.click()
            urlretrieve(img_url, os.path.join(target_dir, 'img%d.jpg' % (i)))
        else:
            # btnext = driver.find_element(By.CSS_SELECTOR, 'a#btnnext.toobar-btn.toobar-btn-next')
            btnnext.click()
            btnpre.click()
            time.sleep(0.5)

    print('%s\t下载完成！' % name)
