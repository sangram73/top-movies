from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Create Table


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img = db.Column(db.String(250), nullable=False)


class RatemovieForm(FlaskForm):
    rating = StringField("Your rateting out of 10 e.g: 6.8")
    review = StringField("Your review  ")
    submit = SubmitField("Done")


class MovieAdd(FlaskForm):
    titel = StringField("type movie name eg: titanic")
    submit = SubmitField("search")

# After adding the new_movie the code needs to be commented out/deleted.
# So you are not trying to add the same movie twice.
# new_movie = Movie(
#     title="Avatar: The Way of Water ",
#     Year=2022,
#     description="Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
#     rating=7.8,
#     ranking=8,
#     review="My favourite character was the sangram",
#     img="https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_FMjpg_UX1000_.jpg"
# )
# with app.app_context():
#     # db.create_all()
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():

    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    form = RatemovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        Movie.rating = float(form.rating.data)
        Movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", Movie=movie, form=form)


@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/add', methods=["GET", "POST"])
def add():
    form = MovieAdd()
    if form.validate_on_submit():
        movie_title = form.titel.data
        response = requests.get(config.endpoin, params={
                                "api_key": config.api_key, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
