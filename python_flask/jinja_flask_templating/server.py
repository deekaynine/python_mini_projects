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
    url = "https://api.npoint.io/efa6acee161e2a74b997"
    response = requests.get(url).json()

    return render_template("index.html", data=response, is_list=is_list)

@app.route('/blog/<num>')
def blog_page(num):
    return render_template("blog.html", num=num)

if __name__ == "__main__":
    app.run(debug=True)
