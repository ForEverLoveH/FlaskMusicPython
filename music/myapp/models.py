from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#创建一个数据表SQLAlchemy链接数据库
db=SQLAlchemy()
class User(db.Model): #数据表1 ，表项为id name、email等
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    e_mail = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    user_type = db.Column(db.Integer,default=0)

class Music(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.String(500))
    ext1= db.Column(db.String(500),default='null')
    ext2 = db.Column(db.String(100), default='null')
    ext3 = db.Column(db.String(100), default='null')
    ext4 = db.Column(db.String(100), default='null')
    ext5 = db.Column(db.String(100), default='null')



#收藏
class Collect(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('music.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='collect_user', lazy=True)
    music= db.relationship('Music', backref='collect_music', lazy=True)


class History(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('music.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='history_user', lazy=True)
    music= db.relationship('Music', backref='history_music', lazy=True)
