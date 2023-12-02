from flask import Flask
from flask import render_template

# Html templates must be in a template file or it wont work

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)