from flask import Blueprint, render_template

from webapp.news.model import News

blueprint = Blueprint("news", __name__)


@blueprint.route("/")
def index():
    title = "Новости Python"
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template("index.html", page_title=title, news_list=news_list)
