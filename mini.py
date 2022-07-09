
from time import sleep
import numpy as np
from selenium import webdriver
import html
from log import *


def get_mini_info() -> tuple:

    text = ''
    image_url = None

    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.add_argument('-headless')

    firefox = webdriver.Firefox(options=firefoxOptions)
    firefox.get('https://www.facebook.com/love11mini')
    sleep(3)
    source_code = firefox.page_source
    firefox.close()

    pos = source_code.find(datetime.now().strftime('%-m/%-d'))
    end_pos = source_code.find('買一送一', pos)

    if pos != -1 and end_pos != -1:
        text = source_code[pos:end_pos+4]
        text = text.replace('＂', '').replace('"', '').replace("'", '')

        # Fetch image url.
        pos = source_code.find('https://scontent-tpe1-1.xx.fbcdn.net/', end_pos+4)
        end_pos = source_code.find('"', pos)

        if pos != -1 and end_pos != -1:
            image_url = html.unescape(source_code[pos:end_pos])

    else:
        log('Failed to fetch info for mini daily drink.', LogType.ERROR)

    return (text, image_url)
