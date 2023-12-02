from flask import Flask
from flask import render_template
import random
import datetime as dt
import requests

app = Flask(__name__)


def is_list(value):
    return isinstance(value, list)

@app.route('/')
def home():
    random_number = random.randint(1,10)
    current_year = dt.datetime.now().year
    return render_template('index.html', num=random_number, year = current_year)

@app.route('/data')
def get_data():
    url = "https://api.npoint.io/efa6acee161e2a74b997"
    response = requests.get(url).json()

    return render_template("index.html", data=response, is_list=is_list)


if __name__ == "__main__":
    app.run(debug=True)
