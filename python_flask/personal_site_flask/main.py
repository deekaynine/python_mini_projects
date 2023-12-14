from flask import Flask, render_template
import requests



app = Flask(__name__)

@app.route('/')
def home():
    data = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    posts = data.json()
    return render_template("index.html", posts=posts)



if __name__ == "__main__":
    app.run(debug=True)