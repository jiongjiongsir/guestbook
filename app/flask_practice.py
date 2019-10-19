from flask import Flask, render_template, request, redirect, url_for, Response, make_response,session,flash
import pymysql.cursors
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('indexs'))
    else:
        return render_template('login.html')
@app.route('/register')
def goregister():
    return render_template('register.html')
@app.route('/indexs')
def indexs():
    connection2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='184lyj', db='guestbook',
                                  charset='utf8mb4')
    cursor2 = connection2.cursor()
    sql2 = "select * from message"
    cursor2.execute(sql2)
    u = cursor2.fetchall()
    datatime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')
    username = session['username']
    print(u)
    if not u:
        tip='None'
        return render_template('index.html',tips=tip,time=datatime,name=username)
    else:
        return render_template('index.html',list=u,time=datatime,name=username)
@app.route('/login',methods=['POST','GET'])
def login():

    connection2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='184lyj', db='paw',
                                  charset='utf8mb4')
    cursor2 = connection2.cursor()
    use=request.form.get("user")
    userpassword = request.form.get("password")
    sql2 = "select * from paw where usename=""'%s'"" and usepaw=""'%s'""" %(use,userpassword)
    print(sql2)
    cursor2.execute(sql2)
    num = cursor2.fetchall()
    if len(num)==1:
        session['username']=use
        session.permanent = True
        return redirect(url_for('indexs'))
    elif len(num)==0:
       error="233"
       return render_template('login.html',error=error)
@app.route('/relogin')
def relog():
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('login'))


@app.route('/registuser', methods=['POST','GET'])
def register():
    user=request.form.get("user")
    password=request.form.get("password")
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='184lyj', db='paw',
                                 charset='utf8mb4')
    sql = "insert into paw values('%s' ,'%s')" % (user, password)
    print(sql)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except:
        error = user+"已经被注册，请重新输入QWQ"
        return render_template('register.html', error=error)
    session['username'] = user
    session.permanent = True
    return redirect(url_for('indexs'))


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    info = request.form.get("message")
    names = get()
    print(info)
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='184lyj', db='guestbook',
                                 charset='utf8mb4')
    datatime=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')
    sql = "insert into message values('%s' ,'%s', '%s')" % (names,info,datatime)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    return redirect(url_for('indexs'))
@app.route('/getsession')
def get():
    return session.get('username')
if __name__ == '__main__':
    app.run(debug=True)
