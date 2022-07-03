
from datetime import datetime


def datetime_description(dt: datetime, show_second: bool = True) -> str:

    description = ''
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    d = datetime(dt.year, dt.month, dt.day)
    diff = (today - d).days

    # Set day.
    if diff == 0:
        description += '今天'
    elif diff == -1:
        description += '明天'
    elif diff == -2:
        description += '後天'
    elif diff == 1:
        description += '昨天'
    elif diff == 2:
        description += '前天'
    elif diff < 0:
        description += str(diff) + '天後'
    else:
        description += str(diff) + '天前'

    # Set hour, minute and second.
    if show_second:
        description += dt.strftime('%H:%M:%S')
    else:
        description += dt.strftime('%H:%M')

    return description
