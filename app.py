import traceback
from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector

conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="root", database="ayuntamiento")
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
        cursor.execute('SELECT * from usuario where idusuario=%s and password=%s', (username,password))
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
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/regist')
def regist():
    return render_template('new_user.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    user = request.args.get('username')
    id_user = request.args.get('id_user')
    password = request.args.get('password')
    id_privilegios = 3
    if  id_user   and  user   and  password:
        cursor.execute('INSERT INTO `usuario` (`idusuario`, `user`, `password`, `idprivilegios`) VALUES (%s, %s, %s, %s)',(id_user,user,password,id_privilegios))
        conn.commit()
        return redirect(url_for('login'))
    else:
        traceback.print_exc()
        #return render_template('handling/error/error-saving-data.html')
    

if __name__ == "__main__":
    app.run(debug=True) 
