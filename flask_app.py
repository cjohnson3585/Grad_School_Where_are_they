from flask import Flask, request, redirect, render_template, url_for
import sys
sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")  #OPTIONAL: Only if need to access Python packages installed on a local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")      #OPTIONAL: Only if you need to add the directory of your flask app

app = Flask(__name__)

from functions.sqlquery import sql_edit_insert,sql_query,authenticate,sql_query2,sql_disconnect


@app.route('/login/', methods=['GET', 'POST'])
def login():
    loggedin=False
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        results = authenticate(''' SELECT * FROM data_table where user_name = ? and password = ?''', (username,password))
        if results:
            return redirect(url_for('home', uname=username))
        else:
            return render_template('login.html', msg='Try Again or Register!')
    return render_template('login.html', msg='')

@app.route('/logout')
def logout():
#    sql_disconnect() 
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        contact  = request.form['email']
        results_auth = authenticate(''' SELECT * FROM data_table where user_name = ?''', (username,))
        if not results_auth:
            sql_edit_insert(''' INSERT INTO data_table (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact,password,location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', ('','','','','','','','',username,contact,password,'') )
            msg = 'INSERT INTO data_table (user_name,contact,password) VALUES ('+username+','+contact+','+password+')'
            return redirect(url_for('home', uname=username))
        else:
            return render_template('register.html', msg='User Name taken, Try Again!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/home/<uname>')
def home(uname):
    results = sql_query(''' SELECT * FROM data_table''')
    # Check if user is loggedin
        # User is loggedin show them the home page
    return render_template('sqldatabase.html', results=results, uname=uname)
    # User is not loggedin redirect to login page

@app.route('/forum/<uname>')
def forum(uname):
    return render_template('forum.html', uname=uname)

@app.route('/profile/<uname>', methods=['POST','GET'])
def profile(uname):
    #get account info
    if request.method == 'POST':
        old_last_name = request.form['old_last_name']
        old_first_name = request.form['old_first_name']
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        school = request.form['school']
        degree = request.form['degree']
        field = request.form['field']
        year = request.form['year']
        current_employer = request.form['current_employer']
        job_title = request.form['job_title']
        user_name = request.form['user_name']
        contact = request.form['contact']
        location = request.form['location']
        sql_edit_insert(''' UPDATE data_table set first_name=?,last_name=?,school=?,degree=?,field=?,year=?,current_employer=?,job_title=?,user_name=?,contact=?,location=? WHERE user_name=? ''', (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact,location,user_name))
        msg = 'Updated, return to Home page!'
        aresults = sql_query2(''' SELECT * FROM data_table where user_name = ?''', (uname,))
        return render_template('profile.html', uname=user_name, aresults=aresults, msg=msg)
    else:
        msg=''
        aresults = sql_query2(''' SELECT * FROM data_table where user_name = ?''', (uname,))
        return render_template('profile.html', uname=uname, aresults=aresults, msg=msg)

@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    if request.method == 'POST':
        old_last_name = request.form['old_last_name']
        old_first_name = request.form['old_first_name']
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        school = request.form['school']
        degree = request.form['degree']
        field = request.form['field']
        year = request.form['year']
        current_employer = request.form['current_employer']
        job_title = request.form['job_title']
        user_name = request.form['user_name']
        contact = request.form['contact']
        sql_edit_insert(''' UPDATE data_table set first_name=?,last_name=?,school=?,degree=?,field=?,year=?,current_employer=?,job_title=?,user_name=?,contact=? WHERE user_name=? ''', (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact,user_name))
        print('SUCCESS!')
        msg = 'Updated!'
        results = sql_query(''' SELECT * FROM data_table''')
        return redirect(url_for('profile', uname=user_name, aresults=results))
    else:
        results = sql_query(''' SELECT * FROM data_table''')
        msg='Not Updated'
        return render_template('update.html', uname=user_name, msg=msg)
#    





@app.route('/dropdown')
def dropdown():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'SELECT * FROM data_table'
    # Check if user is loggedin
        # User is loggedin show them the home page
    return render_template('sqldatabase.html', results=results, msg=msg)#, username=session['username'])
    # User is not loggedin redirect to login page
    
@app.route('/hidedata')
def hide_data():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'SELECT * FROM data_table'
    # Check if user is loggedin
        # User is loggedin show them the home page
    return render_template('sqldatabase.html', results=results, msg=msg)#, username=session['username'])
    # User is not loggedin redirect to login page

   
@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        school = request.form['school']
        degree = request.form['degree']
        field = request.form['field']
        year = request.form['year']
        current_employer = request.form['current_employer']
        job_title = request.form['job_title']
        user_name = request.form['user_name']
        contact = request.form['contact']
        sql_edit_insert(''' INSERT INTO data_table (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact) VALUES (?,?,?,?,?,?,?,?,?,?) ''', (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'INSERT INTO data_table (first_name,last_name,school,degree,field,year,current_employer,job_title,user_name,contact) VALUES ('+first_name+','+last_name+','+school+','+degree+','+field+','+year+','+current_employer+','+job_title+','+user_name+','+contact+')'
    return render_template('sqldatabase.html', results=results, msg=msg) 





@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'GET':
        lname = request.args.get('lname')
        fname = request.args.get('fname')
        sql_delete(''' DELETE FROM data_table where first_name = ? and last_name = ?''', (fname,lname) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'DELETE FROM data_table WHERE first_name = ' + fname + ' and last_name = ' + lname
    return render_template('sqldatabase.html', results=results, msg=msg)

@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    if request.method == 'GET':
        elname = request.args.get('elname')
        efname = request.args.get('efname')
        eresults = sql_query2(''' SELECT * FROM data_table where first_name = ? and last_name = ?''', (efname,elname))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', eresults=eresults, results=results)



if __name__ == "__main__":
    app.run(debug=True)

