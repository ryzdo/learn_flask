from flask_sqlalchemy import SQLAlchemy, model

# from sqlalchemy.orm import decl_api

db = SQLAlchemy()
base: model = db.Model


class News(base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<News {} {}>".format(self.title, self.url)


if __name__ == "__main__":
    new_news = News()
