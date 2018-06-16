from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Свежие новости')


@app.route('/all')
def all():
    return render_template('all_news.html')


@app.route('/login', methods=['POST'])
def login():
    return render_template('login.html', email=request.form.get('email'), password=request.form.get('password'))


if __name__ == '__main__':
    app.run(debug=True)
