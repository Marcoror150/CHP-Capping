from flask import Flask, request, redirect, render_template, session, flash, jsonify, url_for
from flask_restful import Resource, Api, reqparse
# from parser import parseFile
from db_helper import *
from werkzeug.utils import secure_filename
from functions import validFile, makeBarGraph, cleanse,makeChartDict
import os


UPLOAD_FOLDER = 'csvs/'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False


# Set a random secret key to be used for the session
app.secret_key = b'\xf9\x8co\xed\xce\xb0\x1a\xc3\xc9\xa8\x08=\xb1\x07Q%}\x16\x8e\x86\x81\xe5\x85\xdd'



# Define port for Flask to run on
port = 8078

@app.route('/', methods=['GET', 'POST'])
def login():
    # We will only be using the POST method, but we must verify
    if request.method == 'POST':
    
        # Get the form data from request
        username = request.form["inputUsername"]
        password = request.form["inputPassword"]
        
        # Check the given credentials against the DB
        user = validateLogin(username,password)
        if user:
        
            # Credentials are valid so create a session
            session['logged_in'] = True
            session['firstName'] = user[0][3]
            session['userType'] = getUserType(username)

            # Landing page for Admin is UserMgt.hmtl
            if(session['userType'] == 'Admin'):
                return redirect('usermgt')
                
            # Landing page for Intern/Super Intern is RecordUpload.html
            elif(session['userType'] in ['Intern','Super Intern']):
                return redirect('recordupload')
                
            # Landing page for View Only is DataReport.html
            elif(session['userType'] == 'View Only'):
                return redirect('datareport')
                
            # Landing page for Root/Full User is Homepage.html
            else:
                return redirect('homepage')
        else:
            # Credentials are not valid, send back to login page
            flash("Invalid login", 'error')
            return render_template('index.html')
    else:
        return render_template('index.html')
        
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect('')

@app.route("/charts", methods=['GET'])
def charts():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    report = request.args.get('report')
    if report != None:
        d = makeChartDict(report)

        title, file_name = makeBarGraph(d)
        return render_template('Charts.html', image=file_name, title=title, data=getSavedReports())

    # Charts.html needs all records from the Graph table in the DB
    data = getSavedReports()

    try:
        latest_report = data[0][3]
        d = makeChartDict(latest_report)
        title, file_name = makeBarGraph(d)
        return render_template('Charts.html', image=file_name, title=title, data=getSavedReports())
    except:
        return render_template('Charts.html', data=getSavedReports())
    
    
@app.route("/datareport", methods=['GET', 'POST']) 
def datareport():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
        
    if request.method == 'POST':
        # try:
        report = request.form.to_dict()
        title, file_name = makeBarGraph(report)

        report_string = ''
        for key, val in report.items():
            report_string += f'{key}:{val},'

        report_string = report_string[:-1]

        storeReport(title,report_string)
        
        # except Exception as e:
        #     print('graphing failed')

        # path = 'static/images/'
        # file_name = f'{file_name}.png'
        # url = f'{path}{file_name}'

        # graph.savefig(file_name)
        # shutil.move(os.path.join('.', file_name), os.path.join(path, file_name))
        return redirect(url_for('charts', image=file_name, title=title))
    else:
        programs = getPopulatedPrograms()
        incident_types = getIncidentTypes()
        return render_template('DataReport.html', programs=programs, incidents=incident_types)
    
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
        
    return render_template('Homepage.html', data=getSavedReports())
    
@app.route("/recordupload", methods=['GET', 'POST'])
def recordupload():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
    
    if request.method == 'POST':
        file = ''
        try:
            file = request.files['file']
            print(file)
        except Exception as e:
            print(e)

        print('BIG FISH')
        # if user does not select file submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and validFile(file.filename):
            print('BIG FISHeeeeeee')
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.close()  


            # try:
                # parseFile(filename)
            # except Exception as e:
            #     print(e)

        programs = getPopulatedPrograms()
        incident_types = getIncidentTypes()

        
        # response = render_template('DataReport.html', programs=programs, incidents=incident_types)
        
        # response = render_template('DataReport.html', programs=programs, incidents=incident_types)
        print('FISHHHHH')
        return redirect(url_for('datareport'))
        
    else:
        programs = getTable('program')
        return render_template('RecordUpload.html', file="Browse to choose file", programs=programs)
    
@app.route("/sqlentry", methods=['GET', 'POST'])
def sqlpage():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
    
    if request.method == 'POST':
        sql = request.form['sql']
        query(sql)
        flash("Query executed","success")
    return render_template('SQLEntry.html')
    
@app.route("/usermgt", methods=['GET','POST'])
def addRemoveUser():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
    
    data = getUsers()
    error = False
    if request.method == 'POST':	
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        
        # Before creating the user entry in the DB, we must validate 4 things:	
        
        # 1. Check if the username is already in the DB
        username = request.form['username']
        if not validateUsername(username):
            username = ""
            flash('Username already exists. Please choose a unique username', 'error')
            error = True
        
        # 2. Check if the password and confirm password fields matched
        password = request.form["password"]
        confPassword = request.form["confPassword"]
        if password != confPassword:
            flash('Passwords do not match', 'error')
            error = True
        
        # 3. Verify the password meets the requirements
        if not verifyPassword(password):
            error = True
        
        # 4. Check that a userType was selected
        userType = request.form["userType"]
        if userType == 'Select One:':
            flash('Please select a valid user type', 'error')
            error = True
        
        # If any of the 4 conditions above failed, we do not create a new entry and tell the user what they did wrong
        if error:
            session['newUser'] = True
            session['newFirstName'] = firstName
            session['newLastName'] = lastName
            session['newUsername'] = username
            return render_template('UserMgt.html',data=data)
            
        # If all 4 conditions passed, then create the entry
        else:
            session['newUser'] = False
            values = [username,password,firstName,lastName,userType]
            createUser(values)
            data = getUsers()
            flash ('User created', 'success')
            return render_template('UserMgt.html',data=data)
            
    return render_template('UserMgt.html',data=data)

@app.route("/deleteUser/<UID>", methods=['GET','POST'])
def deleteUser(UID):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
    
    try:
        int(UID)
        removeUser(UID)
        flash('User deleted', 'success')
        data = getUsers()
        return redirect('usermgt')
        
    except Exception as e:
        print (e)
        return redirect('usermgt')

@app.route("/changePermission/<UID>/<userType>", methods=['GET','POST'])
def changePermission(UID,userType):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
        
    try:
        # Leave the next 2 lines. Temporary fix for bug where this route 
        # is called twice with CHPLogo.png as the UID and userType.
        int(UID)
        str(userType)
        
        changeUserType(UID,userType)
        flash('Successfully changed user permissions', 'success')
        data = getUsers()
        return redirect('usermgt')
        
    except Exception as e:
        print (e)
        return redirect('usermgt')
        
@app.route("/changePassword/<UID>/<newPassword>/<confNewPassword>", methods = ['GET','POST'])
def changePassword(UID,newPassword,confNewPassword):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
    
    # Verify that passwords matched
    if newPassword != confNewPassword:
        flash('Passwords did not match, user password was not changed.', 'error')
    elif verifyPassword(newPassword):
        changeUserPassword(UID,newPassword)
        flash('Successfully changed user password', 'success')
    else:
        flash('User password was not changed.','error')
        
    return redirect('usermgt')
    
@app.route("/getTable/<table>", methods=['GET'])
def getTableJson(table):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
        
    rows = getTable(table)
    cols = [col[0] for col in getTableCols(table,True)]
    table = []
    for row in rows:
        table.append(dict(zip(cols, row)))
    return jsonify(table), 200

@app.route("/getChildrenProgram/<program>", methods=['GET'])
def childrenProgram(program):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    
    rows = getChildrenProgram(program)
    table = []
    for row in rows:
        table.append(row[0])
    return jsonify(table), 200
    
@app.route("/deleteReport/<GID>", methods=['GET','POST'])
def deleteReport(GID):
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    elif session['userType'] == 'Full User':
        return redirect('/homepage')
    elif session['userType'] in ['Intern','Super Intern']:
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/datareport')
        
    try:
        # Leave this line. Temporary fix for bug where this route 
        # is called twice with CHPLogo.png as the GID.
        int(GID)

        removeReport(GID)
        flash('Report deleted', 'success')
        return redirect('charts')
    except Exception as e:
        print (e)
        return redirect('charts')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
