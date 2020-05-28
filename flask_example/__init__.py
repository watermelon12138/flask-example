# coding:utf-8
from flask import Flask
from flask_example.data import db
from config import DevelopmentConfig
from flask_example.word_count.views import word_count

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# 注册蓝图
app.register_blueprint(word_count)