from flask import Flask, render_template
import requests

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/<int:post_id>')
def single_post(post_id):
    post = posts[0]
    print(post)
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)