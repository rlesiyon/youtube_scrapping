import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium_scrape import setup_selenium_scroller, json_data


def process_soup_data(data):
    scripted_data = data['contents']['twoColumnBrowseResultsRenderer']['tabs']

    watch_video_history = []

    for d in scripted_data:
        for _ in d['tabRenderer']['content']['sectionListRenderer']['contents']:
            try:
                for renderer_object in _['itemSectionRenderer']['contents']:
                    if list(renderer_object.keys())[0] == 'videoRenderer':
                        watch_video_history.append(video_renderer_data(
                            renderer_object['videoRenderer']))
            except Exception as e:
                pass

    return watch_video_history

def video_renderer_data(video_dict):
    video = {
        'videoId': video_dict['videoId']
    }

    title_string = []
    for title_runs in video_dict['title']['runs']:
        title_string.append(title_runs['text'])
    video['title'] = " ".join(title_string)

    return video

def saving_file_txt(filename, data) -> None:
    with open(filename, 'w') as fp:
        for d in data:
            fp.write(
                f"{d['videoId']}__{d['title']}__{d['label']}__{d['view']}__{d['isWatched']}")
            fp.write('\n')

def url_requests(url, headers):

    response = requests.get(url, headers=headers)
    page_soup = bs(response.text, "lxml")
    script = page_soup.findAll('script')[-6]
    json_text = re.search(
        'var ytInitialData = (.+)[,;]{1}', str(script)).group(1)

    return json.loads(json_text)

def parse_html_lxml(page):
    page_soup = bs(page, "lxml")
    script = page_soup.findAll('script')[-6]
    json_text = re.search(
        'var ytInitialData = (.+)[,;]{1}', str(script)).group(1)
    return json.loads(json_text)


if __name__ == '__main__':

    print('Starting')
    HEADERS = json_data('../headers.json')
    # watch_history = process_soup_data(url_requests(URL, headers=HEADERS))
    # print(pd.DataFrame(watch_history).drop_duplicates().to_markdown())
    TIME_SLEEP = 10
    MAX_TRIALS = 3
    URL = "https://www.youtube.com/results?search_query=kenya"
    root_url = 'https://www.youtube.com'
    cookie = HEADERS['cookie']

    driver = setup_selenium_scroller(root_url,
                            URL, cookie, MAX_TRIALS, TIME_SLEEP)                        
    pd.DataFrame(process_soup_data(parse_html_lxml(driver.page_source))).drop_duplicates().to_csv('youtube_search_kenya.csv')