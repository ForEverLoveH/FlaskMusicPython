
from flask import  Flask
from myapp.views import blue,admin
import os
from myapp.models import db



def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app=Flask(__name__,static_folder=static_dir,template_folder=templates_dir)

    app.register_blueprint(blueprint=blue,url_prefix='/user')
    app.register_blueprint(blueprint=admin, url_prefix='/admin')
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:mysql@127.0.0.1:3306/music'
    app.config['DEBUG']=True
    app.config['SECRET_KEY'] = '123456'
    app.config['UPLOAD_FOLDER']='C:\\Users\\HK\\Desktop\\python\\flask_test\\uploadfiles'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    app.config['NAME_SERVER']='stmp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = '1227494175@qq.com'
    app.config['MAIL_PASSWORD'] = 'cwxwan123.'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = True
    app.config['SQLALCHEMY_COMMIT_TEARDOWN '] = True

    db.init_app(app)
    return app

BASE_DIR = os.path.dirname(__file__)
