
import matplotlib.pyplot as plt
import numpy as np
import requests
from log import *
from secret import get_const_weather_key


def get_rain_info() -> tuple:

    parameters = {
        'key': get_const_weather_key(),
        'q': '22.8939153,120.1822497',
        'days': '1'
    }

    resp = requests.get('http://api.weatherapi.com/v1/forecast.json', params=parameters)

    if resp.status_code == 200:
        will_it_rain_hourly = []
        chance_of_rain_hourly = []

        try:
            resp = resp.json()
            hours_data = resp['forecast']['forecastday'][0]['hour']

            for hour_data in hours_data:
                will_it_rain_hourly.append(hour_data['will_it_rain'])
                chance_of_rain_hourly.append(hour_data['chance_of_rain'])

            if len(will_it_rain_hourly) != len(chance_of_rain_hourly):
                raise Exception('Data from api are wrong. The api may be changed.')

        except Exception as e:
            log(e, LogType.ERROR)
            return

        else:
            text = ''
            chart = None

            """
                Deal with text.
            """

            time_set = []
            time_set_formatted = []

            for i in range(len(will_it_rain_hourly)):
                if will_it_rain_hourly[i] == 1:
                    time_set.append(i)

            i = 0
            while i < len(time_set):
                start = i

                while i + 1 < len(time_set):
                    i += 1

                    if time_set[i-1] + 1 != time_set[i]:
                        i -= 1
                        break

                if start == i:
                    time_set_formatted.append(str(time_set[i]) + ':00~' + str(time_set[i]) + ':59')
                else:
                    time_set_formatted.append(str(time_set[start]) + ':00~' + str(time_set[i]) + ':59')

                i += 1

            for period in time_set_formatted:
                text += '今天 ' + period + ' 會有降雨，請留意天氣狀況並攜帶雨具。\n'

            if len(text) > 0:
                text = '茄萣地區降雨概況如下：' + text

            fig, ax = plt.subplots()

            bar_list = ax.bar(np.arange(24), chance_of_rain_hourly, width=1, color='#399AFF', edgecolor="#004185", linewidth=1)

            for i in range(24):
                if will_it_rain_hourly[i] == 1:
                    bar_list[i].set_color('#0361C6')

            ax.set_xlim(0, 23)
            ax.set_ylim(0, 100)
            ax.set_xlabel('Hour')
            ax.set_ylabel('Raining Rate')
            ax.set_xticks(np.arange(0, 24, 1))
            ax.set_title('Hourly Raining Rate in Qieding District')

            fig.canvas.draw()
            chart = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            chart = chart.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            plt.close(fig)

            return (text, chart)

    else:
        log('Failed to fetch weather data. Http status code is {}.'.format(resp.status_code), LogType.ERROR)
