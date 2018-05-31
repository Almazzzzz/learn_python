import os
import requests
from datetime import date
from flask import Flask, abort, request, render_template
import config
from req import get_weather
from news_list import all_news

city = 'London'
country = 'uk'
template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def index():
    return 'Hi there!'


@app.route('/weather')
def weather():
    url = 'http://samples.openweathermap.org/data/2.5/' \
          f'weather?q={city},{country}&appid={config.weather_appid}'

    weather = get_weather(url)
    now = date.today().strftime('%d.%m.%Y')
    result = f'<p><strong>Сегодня:</strong> {now}</p>' \
             f"<p><strong>Город:</strong> {weather['name']}</p>" \
             f"<p><strong>Температура:</strong> {weather['main']['temp']}</p>"
    return result


@app.route('/news/<int:news_id>')
def news_by_id(news_id):
    news_to_show = [news for news in all_news if news['id'] == news_id]
    if len(news_to_show) == 1:
        result = '<h1>%(title)s</h1><p><i>%(date)s</i></p><p>%(text)s</p>'
        result = result % news_to_show[0]
        return result
    else:
        abort(404)


@app.route('/news')
def news():
    colors = ['green', 'red', 'blue', 'black', 'magenta']
    try:
        limit = int(request.args.get('limit'))
    except (ValueError, TypeError):
        limit = 0
    if request.args.get('color') in colors:
        color = request.args.get('color')
    else:
        color = 'black'

    return f'<h1 style="color: {color}">Новости: <small>{limit}</small></h1>'


@app.route('/names')
def names():
    url = 'http://api.data.mos.ru/v1/datasets/' \
          f'2009/rows?api_key={config.data_mos_api_key}'
    result = requests.get(url)

    try:
        year = int(request.args.get('year'))
    except (ValueError, TypeError):
        year = None

    if result.status_code == 200:
        names = result.json()
        if year:
            names = [name for name in names if name['Cells']['Year'] == year]
        return render_template('names.html', names=names)
    else:
        return f'Ошибка: {result.status_code}'


if __name__ == '__main__':
    app.run()
