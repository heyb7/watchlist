import os, sys
from flask import Flask
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# @app.route('/')
# def hello():
#     return 'Welcome to My Watchlist!'

@app.route('/welcome')
def welcome():
    return '欢迎来到我的watchlist!'

@app.route('/hello1')
def hello1():
    return "<h1>Hello Totoro!</h1><img src='http://helloflask.com/totoro.gif'/>"


@app.route('/user/<name>')
def user(name):
    return "<h1>Welcome %s</h1>" % name

@app.route('/test')
def test_url_for():
    # print(url_for('hello'))
    print(url_for('welcome'))
    print(url_for('user',name='heyb'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', name='heyb'))
    return 'Test Page'


import click
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
def forge():
    db.create_all()

    name = 'heyb'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)
    # return render_template('index.html', name=name, movies=movies)