from flask import Flask, render_template
import os


app = Flask(__name__)
app.config['TEMPLATE_FOLDER'] = 'templates'


@app.route('/')
def index_view():
    print(os.getcwd())
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8001)