import json
import os
import time

import polars as pl
from pytube import extract
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

HEADERS_PATH_FILE = '../headers.json'

def is_video_scraped(videoid, filename):
    '''
    The use of polar lazy query to effectively check if a video id is already stored in the csv file.
    '''
    q = (
        pl.scan_csv(filename)
        .filter(pl.col('videoId') == videoid)
    )
    return q.collect().is_empty()

def load_youtube_data_with(driver, filename):

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="contents"]/ytd-video-renderer'))
    )
    youtube_data = driver.find_elements(
        By.XPATH, '//*[@id="contents"]/ytd-video-renderer')

    youtube_data_list = []
    for video in youtube_data:
        try:
            element = video.find_element(
                By.XPATH, './/*[@id = "video-title"]')
            video_id = extract.video_id(element.get_attribute('href'))
            if is_video_scraped(video_id, filename):
                youtube_data_list.append({
                    'videoId': video_id
                })
        except Exception as e:
            pass

    return youtube_data_list

def scroller(driver, time_sleep):

    previous_height = driver.execute_script("return document.documentElement.scrollHeight")

    while (True):
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(time_sleep)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def max_trials(max_trials, time_sleep, driver) -> None:
    trials = 0
    while trials < max_trials:
        print(trials)
        time.sleep(20)
        print(len(driver.find_elements(
            By.XPATH, '//*[@id="contents"]/ytd-video-renderer')))
        scroller(driver, time_sleep)
        trials += 1

def parse_web_cookie(cookie):
  cookies = []

  for cookie_pair in cookie.split(';'):
    if cookie_pair.find('&') == -1:
      name, value = cookie_pair.split('=')
      cookies.append({'name': name.strip(), 'value': value.strip()})
    else:
      pos = cookie_pair.find('=')
      name = cookie_pair[:pos]
      value = cookie_pair[pos+1:]
      cookies.append({'name': name.strip(), 'value': value.strip()})
  return cookies
  
def add_cookie_wrapper(url, cookie, web_driver) -> None:
    '''
    Wraps on the add_cookie method used in selenium webdriver. This methods uses a general entrypoint (url) that does not require cookie. These entry point is then used to set the cookies for more specific url access. 

    Args: 
        url: root-url
        cookie: a list of cookies with name, and value
        web_driver: instance of selenium webdriver
    '''

    web_driver.get(url)
    for cookie in parse_web_cookie(cookie):
        web_driver.add_cookie(cookie)

def json_data(file_name):

  with open(file_name) as f:
    file_contents = f.read()
  return json.loads(file_contents)

def setup_selenium_scroller(root_url, specific_url, cookie, trials, time_sleep, cookie_needed = False):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    if cookie_needed:
        add_cookie_wrapper(root_url, cookie, driver)

    driver.get(url=specific_url)
    max_trials(trials, time_sleep, driver)
    return driver
    
    



