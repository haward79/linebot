
from secret import get_const_linebot_userid
from weather import *
import linebot


def rain_alert():

    messages = []
    (text, chart) = get_rain_info()

    if len(text) > 0:
        messages = linebot.append_message(linebot.create_text_message(text), messages)

    if len(messages) > 0:
        linebot.push(get_const_linebot_userid(), messages)


rain_alert()
