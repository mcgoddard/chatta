from flask import Flask, render_template, request, redirect, escape, session, url_for, flash

import database, hashlib, models, time, datetime, json

from database import db_session

from models import User, Message

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    if 'username' in session:
        thisuser = User.query.filter(User.username == session['username']).first()
        now = datetime.datetime.now()
        thisuser.active_until = now + datetime.timedelta(seconds = 30)
        db_session.commit()
        messages = Message.query.all()
        active_users = User.query.filter(User.active_until > datetime.datetime.now())
        return render_template('chat.html', name = session['username'], messages = messages, users = active_users, now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('index.html')

@app.route('/update')
def update():
    if 'username' in session:
        last_update = request.args.get('last_update','')
        if last_update != '':
            try:
                last_datetime = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
                thisuser = User.query.filter(User.username == session['username']).first()
                now = datetime.datetime.now()
                thisuser.active_until = now + datetime.timedelta(seconds = 30)
                db_session.commit()
                new_messages = Message.query.filter(Message.created_at > last_datetime)
                parsed_new_messages = []
                for message in new_messages:
                    parsed_new_messages.append(dict([("username", message.user.username), ("text", message.text), ("created_at", message.created_at.strftime('%Y-%m-%d %H:%M:%S'))]))
                active_users = User.query.filter(User.active_until > datetime.datetime.now())
                parsed_active_users = []
                for user in active_users:
                    parsed_active_users.append(user.username)
                result = dict([("new_messages", parsed_new_messages), ("active_users", parsed_active_users), ("last_updated", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))])
                return json.dumps(result)
            except ValueError:
                return ""
    return ""

@app.route('/send_message')
def sendMessage():
    if 'username' in session:
        message = request.args.get('message','')
        thisuser = User.query.filter(User.username == session['username']).first()
        if message != '':
            new_message = Message(message, thisuser)
            db_session.add(new_message)
            db_session.commit()
    return ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        if request.method == 'POST':
            salt = "fewnoi*hduw&Sqywe"
            if User.query.filter(User.username == request.form['username'], User.password == hashlib.sha512(request.form['password'] + salt).hexdigest()).first() != None:
                flash('Login successful!','success')
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                flash('No user found matching that username and password!','danger')
                return redirect(url_for('login'))
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' not in session:
        if request.method == 'POST':
            if User.query.filter(User.username == request.form['username']).first() == None:
                salt = "fewnoi*hduw&Sqywe"
                u = User(request.form['username'], hashlib.sha512(request.form['password']+salt).hexdigest())
                db_session.add(u)
                db_session.commit()
                session['username'] = request.form['username']
                flash('Account created!','success')
                return redirect(url_for('index'))
            else:
                flash('That username is taken!','danger')
        return render_template('signup.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'tEt90^}\F:|k1`lyZ.-*!i{gVd"*^qbl-SfR)\&p<*K*u!n5:k/Z>&mX.|"D2]@'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)