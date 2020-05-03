from datetime import datetime, timedelta, timezone
from itertools import groupby

from flask import redirect, render_template, request, url_for
from more_itertools import ilen

from .models import Bingo, app, data, db

JST = timezone(timedelta(hours=9), "JST")
# locale.setlocale(locale.LC_ALL, "ja_JP.UTF-8")


def get_bingo(user, prob):
    return db.session.query(Bingo).filter(Bingo.user == user, Bingo.prob == prob)


@app.route("/")
def index():
    return render_template("index.html", title="最適化モデル演習")


@app.route("/admin")
def admin():
    return render_template("admin.html", title="管理")


@app.route("/login", methods=["POST"])
def login():
    form = request.form
    user = form["user"]
    if user == "admin":
        return redirect(url_for("admin"))
    elif user:
        return redirect(url_for("probs", user=user))
    else:
        return redirect(url_for("index"))


@app.route("/probs/<user>")
def probs(user):
    problist = [
        (bool(get_bingo(user, prob).scalar()), prob, dc["name"],)
        for prob, dc in data["probs"].items()
    ]
    return render_template("probs.html", title="問題一覧", user=user, problist=problist)


@app.route("/prob/<user>/<prob>")
def prob(user, prob):
    ok = bool(get_bingo(user, prob).scalar())
    return render_template(
        "prob.html", title="問題", user=user, prob=prob, data=data, ok=ok
    )


def check(cont, form, key):
    lst = form.getlist(key)
    return not any(
        (str(i) in lst) ^ it.startswith("*") for i, it in enumerate(cont[key])
    )


@app.route("/answer/<user>/<prob>", methods=["POST"])
def answer(user, prob):
    cont = data["probs"][prob]
    form = request.form
    ok = all(check(cont, form, key) for key in ["vars", "objs", "conds"])
    if ok:
        get_bingo(user, prob).delete()
        created_at = datetime.now(JST).replace(microsecond=0)
        db.session.add(Bingo(user=user, prob=prob, created_at=created_at))
        db.session.commit()
        message = f"正解<hr><a href='/probs/{user}'>問題一覧</a>"
    else:
        message = f"残念<hr><a href='javascript:history.back()'>戻る</a>"
    return render_template("message.html", title="判定", user=user, message=message)


@app.route("/users")
def users():
    bingos = Bingo.query.all()
    n = len(data["probs"])
    group = [
        (user, 100 * ilen(gr) // n)
        for user, gr in groupby(bingos, key=lambda bng: bng.user)
    ]
    return render_template("users.html", title="ユーザ 一覧", group=group)


@app.route("/logs")
def logs():
    bingos = Bingo.query.all()
    return render_template("logs.html", title="ログ一覧", bingos=bingos)


@app.route("/clear/<user>")
def clear(user):
    if user == "all":
        db.session.query(Bingo).delete()
    else:
        db.session.query(Bingo).filter(Bingo.user == user).delete()
    db.session.commit()
    return redirect(url_for("users"))
