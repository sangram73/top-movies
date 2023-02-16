from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create Table
class Movie(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(250),unique=True,nullable=False)
    Year =db.Column(db.Integer,nullable=False)
    description =db.Column(db.String(500),nullable=False)
    rating=db.Column(db.Float,nullable=True)
    ranking =db.Column(db.Integer,nullable=True)
    review=db.Column(db.String(250),nullable=True)
    img=db.Column(db.String(250),nullable=False)
db.create_all()
    


    

    

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
