from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/signin', methods =['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM ACCOUNT WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            passCheck = "SELECT UPASSWORD FROM ACCOUNT WHERE username =?"
            stmt = ibm_db.prepare(conn, passCheck)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.execute(stmt)
            result = ibm_db.fetch_assoc(stmt)
            passWordInDb = result["UPASSWORD"]
            if passWordInDb == password:
                session['loggedin'] = True
                #session['id'] = account['UID']
                session['username'] = account['USERNAME']
                msg = 'Logged in successfully !'
                return render_template('dashboard.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
        
        else:
            msg = 'Incorrect username / password !'
        ''' if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) '''
        
    return render_template('signin.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('signin'))
 
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        sql = "SELECT * FROM ACCOUNT WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            msg = 'Account already exists !'
        else:
            insert_sql = "INSERT INTO ACCOUNT VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, lname)
            ibm_db.bind_param(prep_stmt, 5, fname)
            ibm_db.execute(prep_stmt)
            msg = 'Data inserted successfully'
    return render_template('signup.html', msg = msg)
