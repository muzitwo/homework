# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# 初始化数据库
def init_db():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()

    # 创建赛事表
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  date TEXT NOT NULL,
                  location TEXT NOT NULL,
                  max_participants INTEGER NOT NULL,
                  current_participants INTEGER DEFAULT 0)''')

    # 创建报名表
    c.execute('''CREATE TABLE IF NOT EXISTS registrations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(event_id) REFERENCES events(id))''')

    # 添加示例数据
    c.execute("INSERT INTO events (name, date, location, max_participants) VALUES (?, ?, ?, ?)",
              ('城市马拉松', '2025-11-15', '市中心体育场', 500))
    c.execute("INSERT INTO events (name, date, location, max_participants) VALUES (?, ?, ?, ?)",
              ('社区篮球赛', '2025-10-20', '区体育馆', 64))

    conn.commit()
    conn.close()


# 首页路由
@app.route('/')
def index():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return render_template('index.html', events=events)


# 报名页面
@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    if request.method == 'POST':
        # 获取表单数据
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # 验证赛事是否存在
        conn = sqlite3.connect('sports.db')
        c = conn.cursor()
        c.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        event = c.fetchone()

        if event and event[5] < event[4]:
            # 添加报名记录
            c.execute("INSERT INTO registrations (event_id, name, email, phone) VALUES (?, ?, ?, ?)",
                      (event_id, name, email, phone))

            # 更新赛事人数
            c.execute("UPDATE events SET current_participants = current_participants + 1 WHERE id = ?", (event_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('success'))
        else:
            return "赛事不存在或已满员", 400

    return render_template('register.html', event_id=event_id)


# 成功页面
@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)