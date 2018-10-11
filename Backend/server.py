from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
      return render_template('index.html')

@app.route("/charts", methods=['GET'])
def charts():
    return render_template('Charts.html')
    
if __name__ == "__main__":
    app.run()