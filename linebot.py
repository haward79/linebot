
import requests
from log import *
from secret import get_const_linebot_key


def create_text_message(text: str) -> dict:

    return {
        'type': 'text',
        'text': text
    }


def create_image_message(image) -> dict:

    # Image have to upload to owncloud and get share link.

    return {
        'type': 'image',
        'originalContentUrl': '',
        'previewImageUrl': ''
    }


def append_message(msg: dict, messages: list) -> list:

    if len(messages) == 5:
        log('Message has reached the maximum: 5. Rest of the messages are truncated.', LogType.ERROR)
        return messages[:5]

    elif len(messages) > 5:
        log('Message has reached the maximum: 5. No more message is appended.', LogType.ERROR)
        return messages.copy()

    else:
        new_message = messages.copy()
        new_message.append(msg)

        return new_message


def push(user_id: str, messages: list) -> bool:

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {' + get_const_linebot_key() + '}'
    }

    data = {
        'to': user_id,
        'messages': messages
    }

    resp = requests.post('https://api.line.me/v2/bot/message/push', headers=header, json=data)

    if resp.status_code == 200:
        return True

    else:
        log(resp.json(), LogType.ERROR)
        return False
