from flask import Flask
from flask import url_for
from flask import render_template

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)