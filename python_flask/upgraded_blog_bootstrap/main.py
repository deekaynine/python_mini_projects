from flask import Flask, render_template, request
from dotenv import load_dotenv
import smtplib
import requests
import os

load_dotenv()

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
OWN_EMAIL = os.getenv("EMAIL")
OWN_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        try:
            data = request.form
            send_email(data["name"], data["email"], data["phone"], data["message"])
            return render_template("contact.html", msg_sent=True)
            print("success")
        except:
            print("fail")
            return render_template("contact.html", msg_sent=False)


@app.route('/<int:post_id>')
def single_post(post_id):
    post = posts[post_id]
    return render_template("post.html", post=post)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)
