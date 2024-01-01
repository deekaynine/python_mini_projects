from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv
import os
import requests

load_dotenv()
MOVIE_DB_SEARCH_URL = os.getenv("MOVIE_DB_SEARCH_URL")
MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")
MOVIE_DB_DETAILS_URL = os.getenv("MOVIE_DB_DETAILS_URL")
MOVIE_DB_POSTER_URL = os.getenv("MOVIE_DB_POSTER_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"

# Wrap bootstrap around app
Bootstrap5(app)

# Create the extension
db = SQLAlchemy()
# initialise the app with the extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


class EditForm(FlaskForm):
    rating = FloatField(label='Your Rating from 1-10', validators=[DataRequired()])
    review = StringField(label='Your Review',
                             validators=[DataRequired(), Length(min=4, max=250,
                                                                message="Password must be 8 characters long")])
    submit = SubmitField(label="Done")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()


    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET","POST"])
def rate_movie():
    form = EditForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie)

@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/add', methods=["GET","POST"])
def add_movie():
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template('select.html', options=data)
    return render_template("add.html", form=form)

@app.route('/select', methods=["GET","POST"])
def add_movie_to_database():
    movie_id = request.args.get("id")
    movie_search_url = f"{MOVIE_DB_DETAILS_URL}/{movie_id}"
    response = requests.get(movie_search_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
    data = response.json()
    new_movie = Movie(
        title=data["title"],
        year=data["release_date"].split('-')[0],
        img_url=f"{MOVIE_DB_POSTER_URL}{data['poster_path']}",
        description=data["overview"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("rate_movie", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)