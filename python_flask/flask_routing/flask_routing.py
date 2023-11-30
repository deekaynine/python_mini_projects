from flask import Flask

app = Flask(__name__)


def make_bold(fn):
    def bolder(*args, **kwargs):
       return f"<b>{fn(*args, **kwargs)}</b>"
    return bolder

# We need endpoint passed in is because we are decorating both "/" routes
# Endpoint lets us differentiate
@app.route("/", endpoint='home')
@make_bold
def home():
    return f"Hello World"


@app.route("/<username>/<one>/<two>", endpoint='greet_user')
@make_bold
def greet_user(username, one, two):
    return f"Hello {username} {one} {two}"


# Here we are using "converter" types in our path where we can accept specific types
# There are string, int, float, path(strings but also accepts "/" slashes) and uuid
@app.route("/username/<string:name>/<path:user_id>")
@make_bold
def greet_user2(name, user_id):
    return f"Hello {name}, your user_id is {user_id}"


if __name__ == "__main__":
    # Debug=True allows auto reload
    app.run(debug=True)


# @app.router is a decorator, a function that nests a function and return it without being invoked "()"
# Add side functionality to nested function and reduces redundant code
# functions are first class objects like string, floats, ints meaning they can be passed in functions and stored in
# variables
