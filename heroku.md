## 前提

Herokuのアカウントを作成しておくこと

https://signup.heroku.com/

## 手順
```
git clone https://github.com/SaitoTsutomu/opt-quest.git
cd opt-quest
heroku login  # ブラウザでログインすること
git remote remove heroku
heroku create --buildpack heroku/python
heroku addons:create heroku-postgresql:hobby-dev
git push heroku master
heroku ps:scale web=1
heroku logs
heroku run python -c "from opt_quest.models import init; init()"
heroku open
```

## 終了

```
heroku ps:scale web=0
```
