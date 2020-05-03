from .views import app, db, index  # noqa


def main():
    # app.debug = True
    app.run(app.config.get("HOST"), app.config.get("PORT"))
