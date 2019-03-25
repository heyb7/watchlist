import os, sys
from flask import Flask
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy 
from flask import request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_login import current_user


app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    # user = User(name=name)
    # db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='he password used to login.')
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('creating user...')
        user = User(username=username, name='admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向会主页
        # 保存表单数据到数据库
        moive = Movie(title=title, year=year)  #创建记录
        db.session.add(moive) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向会主页

    # user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
    # return render_template('index.html', name=name, movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    return render_template('404.html'), 404

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向会主页
        
        moive.title = title  # 更新标题
        movie.year = year    # 更新年份
        db.session.commit()   # 提交数据库会话
        flash('Item updated') 
        return redirect(url_for('index'))  # 重定向回主页

    print('title: %s' % movie.title)
    return render_template('edit.html', movie=movie)   # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()

    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')