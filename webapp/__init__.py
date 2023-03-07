from flask import Flask, render_template
from webapp.python_org_news import get_python_news
from webapp.model import db, News

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = "Новости Python"
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, news_list=news_list)
    return app