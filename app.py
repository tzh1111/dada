from flask import Flask, request, redirect, url_for, session, flash
from forms import LoginForm, InfoForm, RecordForm, GroupForm, DialogForm, CommentForm, JoinForm
from flask import render_template
from flask_wtf.csrf import CsrfProtect
from models import User, Record, Group, Dialog, Comment, Relation_control, Friend_control
from functools import wraps
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
# from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import logout_user
import os
import logging
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot.corpus

user_info_global = {}

app = Flask(__name__)
'''
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:qwerty1601@127.0.0.1:3306/company"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
'''
app.secret_key = os.urandom(24) # 设置session密钥
'''
app.config['SECRET_KEY'] = 'secret_key' # 设置连接的redis数据库 默认连接到本地6379
app.config['SESSION_TYPE'] = 'redis' # 设置远程
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
db.init_app(app=app)
'''

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)


# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('login', next=request.url))
        if current_user.is_active:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/register', methods={'POST', 'GET'})
def register():
    # 表单对象
    form = InfoForm()
    if form.validate_on_submit():
        user_id = request.form.get('user_id', None)
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        sex = request.form.get('sex', None)
        birthday = request.form.get('birthday', None)
        # 实现注册，保存信息到User模型中
        user = User(user_id)
        user.save_password(password)
        user.insert_info(user_name, sex, birthday)
        login_user(user)
        app.logger.info('user: ' + user.user_email + ' sign in')
        return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods={'POST', 'GET'})
def login():
    # print('-------------------')
    form = LoginForm()
    if form.validate_on_submit():
        user_id = request.form.get('username', None)
        print(user_id)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(user_id)
        print(user.user_email)
        print("kkkk")
        flag = user.get_password_hash()
        if not flag:
            # error = 'Invalid credentials'
            print("gg!")
            flash(u'Invalid password provided', category='error')
            return render_template('login.html', title="Sign In", form=form)

        if check_password_hash(user.password_check, password):
            login_user(user, remember=remember_me)
            # current_user._get_current_object()
            app.logger.info('user: ' + user.user_email + ' login')
            return redirect(request.args.get('next') or url_for('index'))
            # return render_template('index.html', name=current_user.user_email)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/', methods={'POST', 'GET'})
@login_required
def index():
    record = Record(current_user.user_email)
    list = record.display()
    print(list)
    request = Relation_control()
    messages = request.show_deal_request(current_user.user_email)
    count = len(messages)
    myfriend = Friend_control()
    cur_friend = myfriend.friend_count(current_user.user_email)
    fcount = len(cur_friend)
    wcnt = ord(current_user.user_email[-1]) % 3
    user_info_global["name"] = current_user.user_email
    user_info_global["f_count"] = fcount
    user_info_global["wcnt"] = wcnt
    user_info_global["mcnt"] = count
    print(wcnt)
    print(ord("a") % 3)
    print(ord("m") % 3)
    return render_template('index.html', name=current_user.user_email, diaries=list, messagenum=count,
                           myID=current_user.user_email, user_info_global=user_info_global)


@app.route('/write', methods={'POST', 'GET'})
@login_required
def write():
    form = RecordForm()
    content = request.form.get('record')
    print(content)
    print(form.validate_on_submit())
    # if request.method == 'POST':
    if form.validate_on_submit():
        print("1111\n")
        content = request.form.get('record')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = current_user.user_email
        print(content, time, user)
        record = Record(user)
        record.create_new_record(time, content)
        return redirect(request.args.get('next') or url_for('index'))
        # time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    return render_template('write.html', title="write diary", form=form, user_info_global=user_info_global)


@app.route('/showgroups/<deletegroup>', methods={'POST', 'GET'})
@login_required
def showgroups(deletegroup):
    # deletegroup
    group = Group()
    if deletegroup == "None":
        print("haha")
    else:
        group.delete_quit_group(current_user.user_email, deletegroup)
        print("haha222")
    info = group.show_group_join(current_user.user_email)
    print(info)
    form = JoinForm()
    if form.validate_on_submit():
        search_result = request.form.get('searching', None)
        search_result = search_result + ",1,!@#$%"
        return redirect(request.args.get('next') or url_for('addgroup', tuple=search_result))
    return render_template('showgroups.html', groups=info, form=form, user_info_global=user_info_global)


@app.route('/managegroup', methods={'POST', 'GET'})
#@login_required
def managegroup():
    form = GroupForm()
    group_show = Group()
    info = group_show.show_group_own(current_user.user_email)
    group_id = request.form.get('group_id')
    print(group_id)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("1111\n")
        group_id = request.form.get('group_id')
        user = current_user.user_email
        print(group_id, user)
        group_new = Group()
        group_new.create_group(user, group_id)
        return redirect(request.args.get('next') or url_for('managegroup'))
    return render_template('managegroup.html', groups=info, form=form, user_info_global=user_info_global)


@app.route('/chat/<groupchoose>', methods={'POST', 'GET'})
#@groupchoose_required
def chat(groupchoose):
    form = DialogForm()
    dialog_show = Dialog()
    info = dialog_show.show_group_dialog(groupchoose)
    if form.validate_on_submit():
        my_chat = request.form.get('my_chat')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = current_user.user_email
        dialog_new = Dialog()
        dialog_new.create_dialog(groupchoose, user, time, my_chat)
       # return redirect(request.args.get('next') or url_for('chat', groupchoose=groupchoose))
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('chat.html', name=groupchoose, msgs=info, form=form, time=time,
                           group=groupchoose, user_info_global=user_info_global)


'''
#msgs=msgs in group choosed
msgs = [
        {
            'mem': '小爱同学',
            'time': '2019-05-23, 7:30pm',
            'msg': '你好，我是小爱同学'
        },
        {
            'mem': '天猫精灵',
            'time': '2019-05-23, 7:40pm',
            'msg': '你好，我是天猫精灵'
        },
        {
            'mem': '小爱同学',
            'time':'2019-05-23, 8:00pm',
            'msg': '天猫精灵，唱拔萝卜'
        }
    ]
return render_template('chat.html', name=groupchoose, msgs=msgs)
'''


@app.route('/weichat/<groupchoose>', methods={'POST', 'GET'})
#@groupchoose_required
def weichat(groupchoose):
    form = DialogForm()
    dialog_show = Dialog()
    info = dialog_show.show_group_dialog(groupchoose)
    my_chat = request.form.get('my_chat')
    if form.validate_on_submit():
        my_chat = request.form.get('my_chat')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = current_user.user_email
        dialog_new = Dialog()
        dialog_new.create_dialog(groupchoose, user, time, my_chat)
        return redirect(request.args.get('next') or url_for('weichat', groupchoose=groupchoose))
    return render_template('weichat.html', name=groupchoose, msgs=info, form=form, user_info_global=user_info_global)


def diarychoose_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        diarychoose = request.args.get('diarychoose')
        diarychoose=-1
        if diarychoose != -1:
            return func(diarychoose)
        else:
            return redirect(url_for('myfriends'))
    return wapper


def groupchoose_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        groupchoose = request.args.get('groupchoose')
        groupchoose=-1
        if groupchoose != -1:
            return func(groupchoose)
        else:
            return redirect(url_for('showgroups'))
    return wapper


@app.route('/messagebox/<response>')
def messagebox(response):
    request_id = ""
    info = response.split(",")
    print(info)
    status = info[0]
    if status == "2":
        print("no_meaning!")
    else:
        request_id = info[1]

    request = Relation_control()

    if status == "deny" or status == "accept" or status == "ignore":
        request.deal_request(status, request_id)

    messages = request.show_deal_request(current_user.user_email)
    user_info_global["mcnt"] = len(messages)
    response = status + "," + request_id
    # messages=[{'id':'message1','when':'2019-09-28','who':'a','which':'group1'}]

    return render_template('messagebox.html', messages=messages, response=response, user_info_global=user_info_global)


@app.route('/addgroup/<tuple>', methods={'POST','GET'})
def addgroup(tuple):
    display_info = []
    info = tuple.split(",")
    searching = info[0]
    adding = info[2]
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    form = JoinForm()
    group = Group()
    group_info = group.search_group(searching)
    request_1 = Relation_control()

    if group_info is not []:
        for row in group_info:
            request_1.check_request(current_user.user_email, row["name"])

    request_info = request_1.show_request(current_user.user_email)

    for item in group_info:
        for item2 in request_info:
            if item2["name"] == item["name"]:
                display_info.append(item2)

    if form.validate_on_submit():
        search_result = request.form.get('searching', None)
        tuple = search_result + "," + adding + "," + adding
        return redirect(request.args.get('next') or url_for('addgroup',tuple=tuple))

    if adding == "!@#$%":
        print("ignore")
    else:
        new_request = request_1.update_request(current_user.user_email, adding, time)

        i = 0
        for item in display_info:
            if item["name"] == new_request["name"]:
                display_info[i] = new_request
                break
            else:
                i = i + 1

    tuple = searching + "," + adding
    return render_template('addgroup.html', groups=display_info, form=form, tuple=tuple, dada=searching,
                           user_info_global=user_info_global)


@app.route('/myfriends/<deleteID>')
def myfriends(deleteID):
    # if deleteID!=none:delete 先删除后查询
    cur_friend = Friend_control()

    if deleteID is not "None":
        cur_friend.delete_friend(current_user.user_email, deleteID)

    myfriends = cur_friend.show_relation(current_user.user_email)
    f_count = len(cur_friend.friend_count(current_user.user_email))
    user_info_global["f_count"] = f_count
    # myfriends = [{'ID':'001','name':'g1','description':'test group'}]
    return render_template('myfriends.html', friends=myfriends, user_info_global=user_info_global)


@app.route('/thisfriend/<friendchoose>')
#@groupchoose_required
def thisfriend(friendchoose):
    cur_user = User(friendchoose)
    friend = cur_user.show_info()
    record = Record(friendchoose)
    diaries = record.display()
    print(diaries)

    '''
    diaries = [
            {
                ''
                'time': '2019-05-23, 7:30pm',
                'content': '你好，我也是小爱同学'
            }
        ]
    '''

    # friend = {'ID':friendchoose,'name':'balabala','others':'anything'}
    return render_template('thisfriend.html', friend=friend, diaries=diaries, user_info_global=user_info_global)


@app.route('/thisdiary/<friend_diary>', methods={'POST', 'GET'})
@login_required
def thisdiary(friend_diary):
    # friendID,diarychoose=friend_diary
    info = friend_diary.split(",")
    diarychoose = info[1]

    cur_user = info[0]
    form = CommentForm()
    diary_show = Record(cur_user)
    diary = diary_show.display_single(diarychoose)
    diary = diary[0]
    comment_show = Comment()
    comments = comment_show.show_group_dialog(diarychoose)
    if form.validate_on_submit():
        comment = request.form.get('comment', None)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record_id = diarychoose
        comment_new = Comment()
        comment_new.create_dialog(record_id, current_user.user_email, time, comment)
        friend_diary = cur_user + "," + diarychoose
        return redirect(request.args.get('next') or url_for('thisdiary', friend_diary=friend_diary))
    return render_template('thisdiary.html', title="Sign In", form=form, diary=diary,
                           comments=comments, user_info_global=user_info_global)


@app.route('/groupmember/<group_addfriend>')
@login_required
def groupmember(group_addfriend):
    # add addfriend
    info = group_addfriend.split(",")
    cur_friend = Friend_control()
    group_id = info[0]
    addfriend = info[1]
    cur_group = Group()

    if addfriend == "None":
        print("ignore")
    else:
        cur_friend.check_relation(current_user.user_email, addfriend)

    f_count = len(cur_friend.friend_count(current_user.user_email))
    user_info_global["f_count"] = f_count
    mems = cur_group.show_member(current_user.user_email, group_id)
    # print(mems)
    # group,addfriend=group_addfriend
    '''
    mems=[
        {
            'ID':'001',
            'name':'a',
            'isfriend':'0'
        }
    ]
    '''
    return render_template('groupmember.html', mems=mems, group=group_id, user_info_global=user_info_global)


mybot = ChatBot(
    'mybot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',#存储的Adapter
)

trainer = ChatterBotCorpusTrainer(mybot)
trainer.train("chatterbot.corpus.chinese")


@app.route("/dada")
def home():
    return render_template("dada.html",user_info_global=user_info_global)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(mybot.get_response(userText))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='logs/pro.log',
                        filemode='w')
    '''
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run()
