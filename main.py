
from secret import get_const_linebot_userid
from weather import *
from mini import *
import linebot


messages = []


def rain_alert():

    global  messages

    (text, chart) = get_rain_info()

    if len(text) > 0:
        messages = linebot.append_message(linebot.create_text_message(text), messages)
    else:
        messages = linebot.append_message(linebot.create_text_message('今天全日無雨 ^_^'), messages)


def mini_notify():

    global messages

    (text, image) = get_mini_info()

    if len(text) > 0:
        messages = linebot.append_message(linebot.create_text_message('米里Mini 今日優惠\n' + text), messages)
    else:
        messages = linebot.append_message(linebot.create_text_message('無法取得米里Mini今天的優惠資訊。'), messages)


rain_alert()
mini_notify()

if len(messages) > 0:
    linebot.push(get_const_linebot_userid(), messages)
