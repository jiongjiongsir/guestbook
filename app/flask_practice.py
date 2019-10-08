from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

app = Flask(__name__)


@app.route('/')
def hello_world():
    connection2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='guestbook',
                                  charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor2 = connection2.cursor()
    sql2 = "select * from message;"
    cursor2.execute(sql2)
    u = cursor2.fetchall()
    return render_template('index.html', list=u)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    info = request.form.get("info")
    print(info)
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='guestbook',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    sql = "insert into message values('jiong' ,'%s', '1')" % info
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    return redirect(url_for('hello_world'))
if __name__ == '__main__':
    app.run(debug=True)
