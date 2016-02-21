# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.support.ui.

def hello():
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome(executable_path=r'D:\devtools\chromedriver_win32\chromedriver.exe')
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

def huoTicket():
    driver = webdriver.Chrome(executable_path=r'D:\devtools\chromedriver_win32\chromedriver.exe')
    driver.maximize_window()

    # 主页/首页

    driver.get("http://piao.huo.com/index/city/shang%20hai")
    cinemaClick = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nav .icon03"))
    )
    cinemaClick.click() # 点击影院按钮

    # 主页/影院

    movie_mode = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.movie_mode"))
    ) # 等待左边的大列表加载结束

    # 获取影院列表信息

    elements = driver.find_elements_by_css_selector('li > div.con_media')
    cinema_list = []
    for e in elements:
        cinema = e.find_element_by_css_selector('a.wordSearch')
        print cinema.text # 影院名称
        cinema_bttn = e.find_element_by_css_selector('a.ticket_btn')
        url = cinema_bttn.get_attribute('href')
        print url # 相对链接
        # cinema_bttn.click() # 这会打开新页面
        cdata = { 'name': cinema.text, 'url': url }
        cinema_list.append(cdata)

    # 测单个电影院
    # cinema_list = [{ 'name': '', 'url': 'http://piao.huo.com/cinema/cinemaInfo/id/1162' }]

    for c in cinema_list:
        print ">>>>>>>>>>>>>",  c['name']
        driver.get(c['url'])
        # movie_choice = driver.find_element_by_css_selector('div.cinchoice')
        movie_choice = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.cinchoice"))
        )
        cho_det_rt = driver.find_element_by_css_selector('div.cho_det_rt')
        index = 0

        while True:
            movie_choice = driver.find_element_by_css_selector('div.cinchoice')
            movie_images = movie_choice.find_elements_by_css_selector('img')
            if index >= len(movie_images):
                break
            # for img in movie_images:
            #     img.click()
            #     h3 = cho_det_rt.find_element_by_css_selector('h3')
            #     print h3.text
            if not movie_images[index].is_displayed():
                # a_r_btn = movie_choice.find_element_by_css_selector('a.r_btn')
                a_r_btn = driver.find_element_by_css_selector('div.cie2 > a.r_btn')
                a_r_btn.click()
                continue
            movie_images[index].click() # Error: Message: element not visible
            driver.implicitly_wait(1) # seconds
            h3 = cho_det_rt.find_element_by_css_selector('h3')
            print h3.text
            index += 1

    driver.close()

    # driver.get("http://piao.huo.com/cinema/index")
    # cinemaElem = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.ID, "cinema_list"))
    # )
    # cinemaPair = cinemaElem.find_element_by_css_selector('li')
    # print cinemaPair
    # val a = cinemaPair.get(0).findElements(By.cssSelector(".busines_title a"))
    # println(cinemaPair.get(0).findElements(By.cssSelector(".busines_title a")).get(0).getText)

# hello()
huoTicket()
