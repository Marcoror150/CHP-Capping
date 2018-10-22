from flask import Flask, request, render_template, session,flash
from db_helper import validateLogin, getUserType

app = Flask(__name__, static_url_path='/static')
app.debug = True

# Set a random secret key to be used for the session
app.secret_key = b'\xf9\x8co\xed\xce\xb0\x1a\xc3\xc9\xa8\x08=\xb1\x07Q%}\x16\x8e\x86\x81\xe5\x85\xdd'

# # Create instance of flask
# app = Flask(__name__)
# Define port for Flask to run on
port = 8080

@app.route('/', methods=['GET', 'POST'])
def login():
	# We will only be using the POST method, but we must verify
	if request.method == 'POST':
	
		# Get the form data from request
		username = request.form["inputUsername"]
		password = request.form["inputPassword"]
		
		# Check the given credentials against the DB
		if validateLogin(username,password):
		
			# Credentials are valid so create a session
			session['logged_in'] = True
			session['username'] = username

			# If user is admin, send them to Admin page. If not an admin, send to Homepage
			if(getUserType(username) == 'admin'):
				return render_template('Admin.html')
			else:
				return render_template('homepage.html')
				
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
    return render_template('DataReport.html')
    
@app.route("/admin", methods=['GET'])
def admin():
    return render_template('Admin.html')
    
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
	return render_template('Homepage.html')
    
@app.route("/recordupload", methods=['GET', 'POST'])
def recordupload():
    return render_template('RecordUpload.html')

@app.route("/reportspage", methods=['GET', 'POST'])    
def reportspage():
    return render_template('ReportsPage.html')
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
