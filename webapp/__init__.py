from flask import Flask, render_template

from webapp.forms import LoginForm
from webapp.model import News, db


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route("/")
    def index():
        title = "Новости Python"
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template("index.html", page_title=title, news_list=news_list)

    @app.route("/login")
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template("login.html", page_title=title, form=login_form)

    return app
