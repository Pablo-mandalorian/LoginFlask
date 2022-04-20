from crypt import methods
from unicodedata import name
from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector

conn = mysql.connector.connect(host="bdjynruf6ziskqxualjp-mysql.services.clever-cloud.com", port="3306", user="ugvjlyd2h3xtnj4v", password="KFYYYo4kzDHYE2AnaZie", database="bdjynruf6ziskqxualjp")
cursor= conn.cursor()

app = Flask(__name__)
app.secret_key="secret key"

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template('home.html', username= session['username'])

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT * from LoginUsers where User=%s and Password=%s', (username,password))
        record = cursor.fetchone()
        if record:
            session['loggedin']=True
            session['username']=record[1]
            return redirect(url_for('home'))
        else:
            msg="Incorrect"

    return render_template('login.html', msg=msg)

@app.route('/cerrar')
def cerrar():
    session.pop('leggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True) 
