from flask import Flask
from flask import url_for


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'

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
    print(url_for('hello'))
    print(url_for('welcome'))
    print(url_for('user',name='heyb'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', name='heyb'))
    return 'Test Page'