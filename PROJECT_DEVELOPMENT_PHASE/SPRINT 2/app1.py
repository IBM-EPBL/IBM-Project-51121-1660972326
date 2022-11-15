from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/userguide')
def userguide():
    return render_template('userguide.html')

@app.route('/addskill')
def addskill():
    skill1 = ""
    skill2 = ""
    skill3 = ""
    user = session['username']
    sql = "SELECT * FROM ACCOUNTSKILL WHERE USERNAME = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.execute(stmt)
    skillres = ibm_db.fetch_assoc(stmt)
    if skillres:
        skill1 = skillres['SKILL1']
        skill2 = skillres['SKILL2']
        skill3 = skillres['SKILL3']
        print(skillres)
        return render_template('addSkill.html', skill1=skill1,skill2=skill2,skill3=skill3)
    else :
        return render_template('addSkill.html', skill1=skill1,skill2=skill2,skill3=skill3)

@app.route('/editskill', methods =['GET', 'POST'])
def editskill():
    usernameskill = session['username']
    sql = "SELECT * FROM ACCOUNTSKILL WHERE USERNAME = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,usernameskill)
    ibm_db.execute(stmt)
    skillres = ibm_db.fetch_assoc(stmt)
    if skillres:
        msg = ""
        skill11 = request.form['skill1']
        skill21 = request.form['skill2']
        skill31 = request.form['skill3']
        print(skill11,"---",skill21,"--",skill31)
        sql = "UPDATE ACCOUNTSKILL SET SKILL1 = ?, SKILL2 = ?, SKILL3 = ? WHERE USERNAME = ?;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,skill11)
        ibm_db.bind_param(stmt,2,skill21)
        ibm_db.bind_param(stmt,3,skill31)
        ibm_db.bind_param(stmt,4,usernameskill)
        print(":::::::::::::::::::::::::::::::::::",sql)
        ibm_db.execute(stmt)
        msg = "Saved Successfully !"
        return render_template('addSkill.html',msg = msg, skill1=skill11,skill2=skill21,skill3=skill31)
    else :
        msg = ""
        skill12 = request.form['skill1']
        skill22 = request.form['skill2']
        skill32 = request.form['skill3']
        print("----------------------,",usernameskill )
        sql = "INSERT INTO ACCOUNTSKILL VALUES (?,?,?,?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,usernameskill)
        ibm_db.bind_param(stmt,2,skill12)
        ibm_db.bind_param(stmt,3,skill22)
        ibm_db.bind_param(stmt,4,skill32)
        print(":::::::::::::::::::::::::::::::::::",sql)
        ibm_db.execute(stmt)
        msg = "Saved Successfully !"
        return render_template('addSkill.html',msg = msg, skill1=skill12,skill2=skill22,skill3=skill32)

@app.route('/jobmarket')
def jobmarket():
    jobids = []
    jobnames = []
    jobimages = []
    jobdescription = []

    sql = "SELECT * FROM JOBMARKET"
    stmt = ibm_db.prepare(conn, sql)
    username = session['username']
    print(username)
    #ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    joblist = ibm_db.fetch_tuple(stmt)
    print(joblist)
    while joblist != False:
        jobids.append(joblist[0])
        jobnames.append(joblist[1])
        jobimages.append(joblist[2])
        jobdescription.append(joblist[3])
        joblist = ibm_db.fetch_tuple(stmt)

    jobinformation = []

    cols = 4
    size = len(jobnames)
    for i in range(size):
        col = []
        col.append(jobids[i])
        col.append(jobnames[i])
        col.append(jobimages[i])
        col.append(jobdescription[i])
        jobinformation.append(col)
    print(jobinformation)

    return render_template('jobmarket.html', jobinformation = jobinformation)

@app.route('/filterjobs')
def filterjobs():
    skill1 = ""
    skill2 = ""
    skill3 = ""
    user = session['username']
    sql = "SELECT * FROM ACCOUNTSKILL WHERE USERNAME = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.execute(stmt)
    skillres = ibm_db.fetch_assoc(stmt)
    if skillres:
        skill1 = skillres['SKILL1']
        skill2 = skillres['SKILL2']
        skill3 = skillres['SKILL3']
        print(skillres)
        jobids = []
        jobnames = []
        jobimages = []
        jobdescription = []

        sql = "SELECT * FROM JOBMARKET"
        stmt = ibm_db.prepare(conn, sql)
        username = session['username']
        print(username)
        #ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        joblist = ibm_db.fetch_tuple(stmt)
        print(joblist)
        while joblist != False:
            jobids.append(joblist[0])
            jobnames.append(joblist[1])
            jobimages.append(joblist[2])
            jobdescription.append(joblist[3])
            joblist = ibm_db.fetch_tuple(stmt)

        jobinformation = []

        cols = 4
        size = len(jobnames)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$4",skill1,skill2,skill3)

        for i in range(size):
            col = []
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",jobdescription[i])
            if jobdescription[i].lower() == skill1.lower() or jobdescription[i].lower() == skill2.lower() or jobdescription[i].lower() == skill3.lower() :
                col.append(jobids[i])
                col.append(jobnames[i])
                col.append(jobimages[i])
                col.append(jobdescription[i])
                jobinformation.append(col)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",jobinformation)

        return render_template('jobmarket.html', jobinformation = jobinformation)

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
 

def applyJob():
    print("-------------------------Function Called")



@app.route('/profile', methods =['GET', 'POST'])
def profile():
    user = session['username']
    sql = "SELECT * FROM ACCOUNT WHERE USERNAME = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    usernameInUser = account['USERNAME']
    userPassword = account['UPASSWORD']
    userEmail = account['EMAILID']
    firstName = account['FIRSTNAME']
    lastName = account['LASTNAME']
    print(account)
    return render_template('profile.html', usernameInUser=usernameInUser,userPassword=userPassword,userEmail=userEmail,firstName=firstName,lastName=lastName)

@app.route('/editProfile', methods =['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        msg = ""
        username = request.form['usernameInUser']
        password = request.form['userPassword']
        email = request.form['userEmail']
        fname = request.form['firstName']
        lname = request.form['lastName']
        sql = "UPDATE ACCOUNT SET UPASSWORD = ?, EMAILID = ?, FIRSTNAME = ?, LASTNAME = ? WHERE USERNAME = ?;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,password)
        ibm_db.bind_param(stmt,2,email)
        ibm_db.bind_param(stmt,3,fname)
        ibm_db.bind_param(stmt,4,lname)
        ibm_db.bind_param(stmt,5,username)
        print(":::::::::::::::::::::::::::::::::::",sql)
        ibm_db.execute(stmt)
        msg = "Saved Successfully !"
        return render_template('profile.html', msg = msg, usernameInUser=username,userPassword=password,userEmail=email,firstName=fname,lastName=lname)

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


@app.route('/jobapplied/<int:jobid>')
def jobappliedFunction(jobid):
    jobid = jobid
    sql = "SELECT JOBCOMPANY FROM JOBMARKET WHERE JOBID =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,jobid)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_assoc(stmt)
    jobname = result['JOBCOMPANY']
    sql = "SELECT COMPANY_EMAIL FROM JOBMARKET WHERE JOBID =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,jobid)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_assoc(stmt)
    jobemail = result['COMPANY_EMAIL']
    print("---------------------------JOB APPLIED--------------------------------",jobid)
    return render_template('fillapplication.html',jobid = jobid, jobname = jobname, jobemail = jobemail)


@app.route('/appliedjob', methods =['GET', 'POST'])
def appliedjob():
    return redirect(url_for('jobsapplied'))
   
   
@app.route('/jobsapplied')
def jobsapplied():
    jobids1 = []        
    jobinformation = []

    sql = "SELECT * FROM APPLIEDJOBS WHERE USERNAME = ?"
    stmt = ibm_db.prepare(conn, sql)
    username = session['username']
    print(username)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    joblist = ibm_db.fetch_tuple(stmt)
    print(joblist)
    while joblist != False:
        print("-----------------------------------------",joblist)
        jobids1.append(joblist[1])
        joblist = ibm_db.fetch_tuple(stmt)
    
    print(jobids1)
    for x in range(len(jobids1)):
        jobids = []
        jobnames = []
        jobimages = []
        jobdescription = []

        print("nnnnnnnnnnnnnnnnnnnnnnnnnnn",len(jobids1))
        sql = "SELECT * FROM JOBMARKET WHERE JOBID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,jobids1[x])
        
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: ",jobids1[x])
        ibm_db.execute(stmt)
        joblist = ibm_db.fetch_tuple(stmt)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",joblist)
        while joblist != False:
            jobids.append(joblist[0])
            jobnames.append(joblist[1])
            jobimages.append(joblist[2])
            jobdescription.append(joblist[3])
            joblist = ibm_db.fetch_tuple(stmt)
        cols = 4
        size = len(jobnames)
        for i in range(size):
            col = []
            col.append(jobids[i])
            col.append(jobnames[i])
            col.append(jobimages[i])
            col.append(jobdescription[i])
            print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCcc",col)
            jobinformation.append(col)
            print(jobinformation)

    
    print("//////////////////////////////////////////////",jobinformation)

    return render_template('appliedjobs.html', jobinformation = jobinformation)
