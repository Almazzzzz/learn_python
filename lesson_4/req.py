import requests


def get_weather(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        return 'Что-то не то'


if __name__ == '__main__':
    data = get_weather('http://samples.openweathermap.org/data/2.5/weather'
                       '?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22')
    print(data)
