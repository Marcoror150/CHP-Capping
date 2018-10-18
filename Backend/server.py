from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__, static_url_path='/static')
app.debug = True

# # Create instance of flask
# app = Flask(__name__)
# Define port for Flask to run on
port = 8080

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
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
