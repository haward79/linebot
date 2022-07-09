
from datetime import datetime
from typing import Union
import numpy as np
import requests
import cv2
from log import *
from secret import get_const_storage_path, get_const_linebot_key


def create_text_message(text: str) -> dict:

    return {
        'type': 'text',
        'text': text
    }


def create_image_message(image: Union[str, np.ndarray]) -> dict:

    if type(image) is np.ndarray:
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        filename_url = 'https://www.haward79.tw/linebot/' + filename

        cv2.imwrite(get_const_storage_path() + filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        return {
            'type': 'image',
            'originalContentUrl': filename_url,
            'previewImageUrl': filename_url
        }

    elif type(image) is str:
        return {
            'type': 'image',
            'originalContentUrl': image,
            'previewImageUrl': image
        }

    else:
        log('Datatype error. Image should be string or numpy array.', LogType.ERROR)

        return None


def append_message(msg: dict, messages: list) -> list:

    if msg is None or messages is None:
        log('Message or Messages is None.', LogType.ERROR)

        return None

    else:
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
