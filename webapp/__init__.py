from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from webapp.model import News, db
from webapp.user.model import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route("/")
    def index():
        title = "Новости Python"
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template("index.html", page_title=title, news_list=news_list)

    @app.route("/admin")
    @login_required
    def admin_index():
        if current_user.is_admin:
            return "Привет админ"
        else:
            return "Ты не админ!"

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
