
from time import sleep
from secret import get_const_linebot_userid
from weather import *
from mini import *
import linebot


messages = []

locations = [
    {
        'name': '茄萣',
        'coordinate': (22.8940952, 120.1821555)
    },
    {
        'name': '臺南',
        'coordinate': (22.9245516, 120.2859521)
    }
]


def rain_alert():

    global messages, locations

    for location in locations:
        (text, chart) = get_rain_info(location['name'], location['coordinate'])

        if len(text) > 0:
            messages = linebot.append_message(linebot.create_text_message(text), messages)
        else:
            messages = linebot.append_message(linebot.create_text_message('今天' + location['name'] + '地區全日無雨 ^_^'), messages)

        messages = linebot.append_message(linebot.create_image_message(chart), messages)

        sleep(1)


def mini_notify():

    global messages

    (text, image_url) = get_mini_info()

    if len(text) > 0:
        messages = linebot.append_message(linebot.create_text_message('米里Mini 今日優惠\n' + text), messages)

        if image_url is not None:
            messages = linebot.append_message(linebot.create_image_message(image_url), messages)
    else:
        messages = linebot.append_message(linebot.create_text_message('無法取得米里Mini今天的優惠資訊。'), messages)


if __name__ == '__main__':
    # Notify rain.
    rain_alert()

    if len(messages) > 0:
        linebot.push(get_const_linebot_userid(), messages)

    messages.clear()


    # Notify mini.
    mini_notify()

    if len(messages) > 0:
        linebot.push(get_const_linebot_userid(), messages)

    messages.clear()
