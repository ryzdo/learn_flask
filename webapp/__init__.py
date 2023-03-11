from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_user

from webapp.forms import LoginForm
from webapp.model import News, User, db


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

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/process-login", methods=["POST"])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Вы вошли на сайт")
                return redirect(url_for("index"))
        flash("Неправильное имя пользователя или пароль")
        return redirect(url_for("login"))

    return app
