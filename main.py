from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def title():
    return render_template('base.html')

@app.route('/countries')
def choose_countries():
    return render_template('countries.html')

@app.route('/country/<name>')
def country(name):
    return render_template(f'{name}.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')