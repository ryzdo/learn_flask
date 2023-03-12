from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

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
        if current_user.is_authenticated:
            return redirect(url_for("index"))
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
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
        flash("Неправильное имя пользователя или пароль")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/admin")
    @login_required
    def admin_index():
        if current_user.is_admin:
            return "Привет админ"
        else:
            return "Ты не админ!"

    return app
