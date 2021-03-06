from flask import Flask, request, redirect, render_template, session, flash, jsonify, url_for
from flask_restful import Resource, Api, reqparse
from db_helper import *
from werkzeug.utils import secure_filename
from functions import validFile, makeBarGraph, cleanse,makeChartDict
from sheet_parser import parseFile
import os


UPLOAD_FOLDER = 'csvs/'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False


# Set a random secret key to be used for the session
app.secret_key = b'\xf9\x8co\xed\xce\xb0\x1a\xc3\xc9\xa8\x08=\xb1\x07Q%}\x16\x8e\x86\x81\xe5\x85\xdd'



# Define port for Flask to run on
port = 8076

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
            session['uid'] = user[0][0]
            session['firstName'] = user[0][3]
            session['UID'] = user[0][0]
            session['userType'] = getUserType(username)

            # Landing page for Admin is UserMgt.hmtl
            if(session['userType'] == 'Admin'):
                return redirect('usermgt')
                
            # Landing page for Intern/Super Intern is RecordUpload.html
            elif(session['userType'] in ['Intern']):
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
    # Clear all session variables upon logout
    session.clear()
    return redirect('')

@app.route("/charts", methods=['GET'])
def charts():
    # Prevent unauthorized access to this page via URL manipulation
    if not session.get('userType'):
        return redirect('')
    report = request.args.get('report')

    # If loading a saved query, chart it
    if report != None:
        d = makeChartDict(report)

        title, file_name = makeBarGraph(d)
        return render_template('Charts.html', image=file_name, title=title, data=getSavedReports())

    # Charts.html needs all records from the Graph table in the DB
    data = getSavedReports()

    # Get the latest report and render it if navigating to the charts page without creating a report
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
        report = request.form.to_dict()

        try:
            # Try to create the chart
            title, file_name = makeBarGraph(report)

            saved_report = request.args.get('report')

            # Check if we are saving the report
            # if saved_report:
            # Create a string that stores the exact query for later use
            report_string = ''
            for key, val in report.items():
                report_string += f'{key}:{val},'

            # Remove the last comma
            report_string = report_string[:-1]

            # Store the query in the db
            storeReport(title,report_string)
            print(file_name)
            # Goto the chart page if a chart is created successfully 
            return redirect(url_for('charts', image=file_name, title=title))
        
        # Flash an error if something goes wrong
        except Exception as e:
            print(e)
            flash("Chart Creation error",'error')
            return redirect('datareport')

    # Render the page
    else:
        programs = getPopulatedPrograms()
        incident_types = getTable('IncidentTypes')
        children = getTable('Children')
        return render_template('DataReport.html', programs=programs, incidents=incident_types, children=children ,port=str(port))
    
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
	# Prevent unauthorized access to this page via URL manipulation
	if not session.get('userType'):
		return redirect('')
	elif session['userType'] == 'Intern':
		return redirect('/recordupload')
	elif session['userType'] == 'View Only':
		return redirect('/datareport')
  
	return render_template('Homepage.html',data1=getUnreviewedReportsSuperInterns(),data2=getUnreviewedReportsInterns(),alldata=getAllUnreviewedReports(),IncidentTypes=getIncidentTypes())
    
@app.route("/createIncident/<KID>/<incidentType>", methods=['GET', 'POST'])
def createIncident(KID,incidentType):
	# Prevent unauthorized access to this page via URL manipulation
  if not session.get('userType'):
    return redirect('')
  elif session['userType'] == 'Intern':
    return redirect('/recordupload')
  elif session['userType'] == 'View Only':
    return redirect('/datareport') 
    
  try:
    # Leave the next 2 lines. Temporary fix for bug where this route 
    # is called twice with CHPLogo.png as the IncidentType
    int(KID)
    int(incidentType)

    createManualIncident(KID,incidentType,session['UID'])
    
    flash("Incident created.","success")
    return redirect('homepage')
        
  except Exception as e:
    print (e)
    return redirect('homepage')
    
@app.route("/createIncidentAccept/<KID>/<incidentType>", methods=['GET', 'POST'])
def createIncidentAccept(KID,incidentType):
	# Prevent unauthorized access to this page via URL manipulation
  if not session.get('userType'):
    return redirect('')
  elif session['userType'] == 'Intern':
    return redirect('/recordupload')
  elif session['userType'] == 'View Only':
    return redirect('/datareport') 
    
  try:
    # Leave the next 2 lines. Temporary fix for bug where this route 
    # is called twice with CHPLogo.png as the IncidentType
    int(KID)
    int(incidentType)

    createManualIncidentAccept(KID,incidentType,session['UID'])
    
    flash("Incident created and accepted.","success")
    return redirect('homepage')
        
  except Exception as e:
    print (e)
    return redirect('homepage')
  
 
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
        except Exception as e:
            print(e)

        # if user does not select file submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and validFile(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.close()  
            program = request.form['program']
            incident_type = request.form['incident']
            uid = session.get('uid')
            try:
                parseFile(filename,program,incident_type,uid)
            except Exception as e:
                print(e)
        flash('File Uploaded')
        return redirect('recordupload')
        # programs = getPopulatedPrograms()
        # incident_types = getIncidentTypes()
        
        # return redirect(url_for('datareport'))
        
    else:
        programs = getTable('program')
        incidents = getIncidentTypes()
        return render_template('RecordUpload.html', file="Browse to choose file", programs=programs,incidents=incidents)
    
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
    
    # Get the user's query and send it to the DB.
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
        
            # These session variables are used to refill the form with the values the user entered before submitting.
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
    elif session['userType'] == 'Intern':
        return redirect('/recordupload')
    elif session['userType'] == 'View Only':
        return redirect('/recordupload')
        
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
		
@app.route("/acceptRecord/<IID>", methods=['GET','POST'])
def acceptRecord(IID):
	acceptReport(IID)
	flash('Record accepted','success')
	return redirect('/homepage')
	
@app.route("/denyRecord/<IID>", methods=['GET','POST'])
def denyRecord(IID):
	denyReport(IID)
	flash('Record rejected','success')
	return redirect('/homepage')
	
@app.route("/acceptAllRecords", methods=['GET','POST'])
def acceptAllRecords():
	acceptAllReports()
	flash('All Full User/Super Intern records accepted','success')
	return redirect('/homepage')
	
@app.route("/pepe", methods=['GET'])
def pepe():
    return render_template('Pepe.html')    

	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)

