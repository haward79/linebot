
from time import sleep
import numpy as np
from selenium import webdriver
from log import *


def get_mini_info() -> tuple:

    text = ''
    image = None

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

    else:
        log('Failed to fetch info for mini daily drink.', LogType.ERROR)

    return (text, image)
