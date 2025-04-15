from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def title():
    return 'Тут будет главная страница сайта'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')