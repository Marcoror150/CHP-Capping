from flask import Flask, request, redirect, render_template, session, flash, jsonify, url_for
from flask_restful import Resource, Api, reqparse
from db_helper import *
from werkzeug.utils import secure_filename
from functions import validFile, makeBarGraph, cleanse


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
	data = getUsers();
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

			# If user is admin, send them to Admin page. If not an admin, send to Homepage
			if(session['userType'] == 'Admin'):
				return redirect('usermgt')
			elif(session['userType'] == 'Intern'):
				return redirect('recordupload')
			elif(session['userType'] == 'View Only'):
				return redirect('datareport')
			else:
				return redirect('homepage')
		else:
			# Credentials are not valid so give error message
			flash("Invalid login", 'error')
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/charts", methods=['GET'])
def charts():
    return render_template('Charts.html')
    
@app.route("/datareport", methods=['GET', 'POST']) 
def datareport():
    if request.method == 'POST':
        # try:
        title, file_name = makeBarGraph(request.form.to_dict())
        # except Exception as e:
        #     print('graphing failed')

        # path = 'static/images/'
        # file_name = f'{file_name}.png'
        # url = f'{path}{file_name}'

        # graph.savefig(file_name)
        # shutil.move(os.path.join('.', file_name), os.path.join(path, file_name))
        return render_template('Charts.html', image=file_name, title=title)
    else:
        programs = getPopulatedPrograms()
        incident_types = getIncidentTypes()
        return render_template('DataReport.html', programs=programs, incidents=incident_types)
    
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
	return render_template('Homepage.html')
    
@app.route("/recordupload", methods=['GET', 'POST'])
def recordupload():
    if request.method == 'POST':
        file = request.files['file']
        
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
            return redirect('/reportspage')
    else:
        programs = getTable('program')
        return render_template('RecordUpload.html', file="Browse to choose file", programs=programs)

@app.route("/reportspage", methods=['GET', 'POST'])    
def reportspage():
    return render_template('DataReport.html')
	
@app.route("/sqlentry", methods=['GET', 'POST'])
def sqlpage():
	if request.method == 'POST':
		sql = request.form['sql']
		query(sql)
		flash("Query executed","success")
	return render_template('SQLEntry.html')
	
@app.route("/usermgt", methods=['GET','POST'])
def addRemoveUser():
	data = getUsers()
	error = False
	if request.method =='POST':	
		firstName = request.form["firstName"]
		lastName = request.form["lastName"]
		
		# Before creating the user entry in the DB, we must validate 3 things:	
		
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
		
		# 3. Check that a userType was selected
		userType = request.form["userType"]
		if userType == 'Select One:':
			flash('Please select a valid user type', 'error')
			error = True
		
		# If any of the 3 conditions above failed, we do not create a new entry and tell the user what they did wrong
		if error:
			session['newUser'] = True
			session['newFirstName'] = firstName
			session['newLastName'] = lastName
			session['newUsername'] = username
			return render_template('UserMgt.html',data=data)
			
		# If all 3 conditions passed, then create the entry
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
	try:
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
	if newPassword != confNewPassword:
		flash('Passwords did not match, user password was not changed.', 'error')
	else:
		changeUserPassword(UID,newPassword)
		flash('Successfully changed user password', 'success')
	return redirect('usermgt')
	
@app.route("/getTable/<table>", methods=['GET'])
def getTableJson(table):
    rows = getTable(table)
    cols = [col[0] for col in getTableCols(table,True)]
    table = []
    for row in rows:
        table.append(dict(zip(cols, row)))
    return jsonify(table), 200

@app.route("/getChildrenProgram/<program>", methods=['GET'])
def childrenProgram(program):
    rows = getChildrenProgram(program)
    table = []
    for row in rows:
        table.append(row[0])
    return jsonify(table), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
