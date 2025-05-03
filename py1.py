from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def title():
    return "Missiya"

@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                 <link rel="stylesheet"
                                 href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                 integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                 crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                <title>Отбор астронавтов</title>
                              </head>
                              <body>
                                <h1 align="center">Загрузка фотографии</h1>
                                <h4 align="center">для участия в миссии</h4>
                                <form method="post" enctype="multipart/form-data">
                                   <div class="form-group">
                                        <label for="photo">Выберите файл</label>
                                        <p></p>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <p></p>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        with open('static/img/my_file.png', 'wb') as file_in:
            data = f.read()
            file_in.write(data)
        return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                 <link rel="stylesheet"
                                 href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                 integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                 crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                <title>Отбор астронавтов</title>
                              </head>
                              <body>
                                <h1 align="center">Загрузка фотографии</h1>
                                <h4 align="center">для участия в миссии</h4>
                                <form method="post" enctype="multipart/form-data">
                                   <div class="form-group">
                                        <label for="photo">Выберите файл</label>
                                        <p></p>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                        <img src="{url_for('static', filename='img/my_file.png')}" 
            alt="здесь должна была быть картинка, но не нашлась">
                                    </div>
                                    <p></p>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                              </body>
                            </html>'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')