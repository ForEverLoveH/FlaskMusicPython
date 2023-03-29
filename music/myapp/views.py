from flask import Blueprint,redirect,render_template,jsonify,request,send_from_directory,Response,make_response,url_for
##redirect 浏览器自动重定向到他的参数所需要的url  render_template将模板转化为完整的html
##jsonify 返回json数据   make_response 实现重定向
from myapp.models import Music,User,db,Collect,History
import  os
import hashlib

blue = Blueprint('user',__name__)
admin = Blueprint('admin',__name__)

@blue.route('/download', methods=['GET', 'POST'])
def download():
    music_id=request.args.get('music_id')
    music=Music.query.filter(Music.id==music_id).first()
    lj = os.path.dirname(os.path.dirname(__file__))
    P=lj+music.path[21:]
    print(P)
    def generate():
        path = P
        with open(path, 'rb') as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)

    return Response(generate(), mimetype="audio/mpeg3",headers={"Content-Disposition": "attachment; filename={0};".format(music.name+'.mp3')})
#返回的对象，再给前端页面传输数据时
#普通用户登陆后首页显示
@blue.route('/index', methods=['GET', 'POST'])
def index():
    keywords=request.args.get('keywords')
    music = Music.query.filter().all()
    if keywords:
        song = Music.query.filter(Music.name == keywords).first()
        if song:
            return render_template('/admin/song_detail.html', song=song)
        else:
            return render_template('/admin/index.html', musics=music)

    return render_template('/admin/index.html',musics=music)

#曲库
@blue.route('/albums_store', methods=['GET', 'POST'])
def albums_store():
    music=Music.query.filter().all()
    return render_template('/admin/albums_store.html',songs=music)

#歌曲详情页
@blue.route('/song', methods=['GET', 'POST'])
def song():
    user_id=request.cookies.get('user_id')
    song_id=request.args.get('song_id')
    history=History.query.filter(History.user_id==user_id).filter(History.song_id==song_id).first()
    if not history:
        h=History()
        h.user_id=user_id
        h.song_id=song_id
        db.session.add(h)
        db.session.commit()
    else:
        db.session.delete(history)
        db.session.commit()
        h = History()
        h.user_id = user_id
        h.song_id = song_id
        db.session.add(h)
        db.session.commit()
    song=Music.query.filter(Music.id==song_id).first()
    return render_template('/admin/song_detail.html',song=song)


#登陆
@blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/admin/user_login.html',message='None')
    email=request.form.get('email')
    password = request.form.get('password')
    music = Music.query.filter().all()
    md5 = hashlib.md5()

    if not all([email,password]):
        return render_template('/admin/user_login.html',message='填写所以信息')
    user=User.query.filter(User.e_mail==email).first()

    if not user:
        return render_template('/admin/user_login.html', message='账户没有注册')
    md5.update(user.password.encode('utf-8'))
    u_password = md5.hexdigest()
    if not u_password==password:
        return render_template('/admin/user_login.html', message='密码错误')
    if user.user_type==1:
        return render_template('/admin/main.html', musics=music)

    res = make_response(redirect(url_for('user.index')))
    res.set_cookie('user_id', str(user.id), max_age=3600)
    return res


#注册
@blue.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method=='GET':
        return render_template('/admin/user_register.html')
    name=request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    if not all([name,email,password]):
        return 'Please enter all information!'
    user=User()
    user.name=name
    user.e_mail=email
    user.password=password
    db.session.add(user)
    db.session.commit()
    return render_template('/admin/user_register.html')

#管理员首页
@admin.route('/main', methods=['GET', 'POST'])
def main():
    musics=Music.query.filter().all()
    return render_template('/admin/main.html',musics=musics)

#添加音乐
@admin.route('/add_music', methods=['GET', 'POST'])
def add_music():
    if request.method=='GET':
        return render_template('/admin/add_music.html', message='None')
    name=request.form.get('name')
    introduce=request.form.get('introduce')
    img=request.files.get('img')
    mp3=request.files.get('mp3')
    singer=request.form.get('singer')

    if not all([name,introduce,img,mp3,singer]):
        return render_template('/admin/add_music.html',message='填写所有信息!')

    music=Music()
    music.name=name
    music.ext2=singer
    music.path='http://127.0.0.1:5000/static/admin/audio/'+mp3.filename
    music.ext3='http://127.0.0.1:5000/static/admin/img/'+img.filename
    music.ext1 =introduce
    db.session.add(music)
    db.session.commit()
    lj=os.path.dirname(os.path.dirname(__file__))
    mp3.save(os.path.join(lj,'static/admin/audio/'+mp3.filename))
    img.save(os.path.join(lj, 'static/admin/img/' + img.filename))
    return render_template('/admin/add_music.html',message='添加成功!')

#删除音乐
@admin.route('/delete_song', methods=['GET', 'POST'])
def delete_song():
    song_id=request.args.get('song_id')
    song=Music.query.filter(Music.id==song_id).first()
    collects=Collect.query.filter(Collect.song_id==song_id).all()
    historys = History.query.filter(History.song_id == song_id).all()
    if collects:
        for item in collects:
            db.session.delete(item)
            db.session.commit()
    if historys:
        for item in historys:
            db.session.delete(item)
            db.session.commit()
    db.session.delete(song)
    db.session.commit()
    musics = Music.query.filter().all()
    return render_template('/admin/main.html', musics=musics)


#个人中心
@blue.route('/user_info', methods=['GET', 'POST'])
def user_info():
    user=User.query.filter(User.id==request.cookies.get('user_id')).first()
    collects=Collect.query.filter().order_by(Collect.create_time.desc()).all()
    history=History.query.filter().order_by(History.create_time.desc()).all()
    data={
        'user':user,
        'collects':collects,
        'history':history
    }
    return render_template('/admin/user_info.html',data=data)


#歌曲详情页
@blue.route('/collect', methods=['GET', 'POST'])
def collect():
    user_id=request.cookies.get('user_id')
    song_id=request.args.get('song_id')
    collect=Collect.query.filter(Collect.user_id==user_id).filter(Collect.song_id==song_id).first()
    if not collect:
        c=Collect()
        c.user_id=user_id
        c.song_id=song_id
        db.session.add(c)
        db.session.commit()
    song=Music.query.filter(Music.id==song_id).first()
    return render_template('/admin/song_detail.html',song=song)

