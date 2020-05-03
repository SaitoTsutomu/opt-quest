import toml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("opt_quest.config")
db = SQLAlchemy(app)

data = toml.load("opt_quest/data.toml")


class Bingo(db.Model):
    __tablename__ = "bingo"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text)
    prob = db.Column(db.Text)
    created_at = db.Column(db.DATETIME)

    def __repr__(self):
        return f"<id={self.user} title={self.prob}>"


def init():
    """
    poetry run python -c "from opt_quest.models import init; init()"
    """
    db.create_all()
