from flask import Flask, render_template, session, redirect, request
import ibm_db
import sys

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID=ghc72736;PWD=cTnreyg6kRM90ju9",'','')
    print("Connected to database")
except:
    print("Unable to connect", ibm_db.conn_errormsg())    


app = Flask(__name__)
app.secret_key = 'supersuper'

@app.route("/")
def homeRoute():
    if 'userId' in session:
        return "<h1>Classy</h1>"
    else:
        return redirect("/login")    

@app.route("/login", methods=['GET', 'POST'])
def loginRoute():
    if  not 'userId' in session:
        if request.method == 'GET':
            return render_template('signin.html')
        else:
            data = request.form
            return str(signInUser(data)) 
    else:
        return redirect("/")            

@app.route("/sign-up", methods=['GET', 'POST'])
def signupRoute():
    if  not 'userId' in session:
        if request.method == 'GET':
            return render_template('signup.html'); 
        else:
            data = request.form
            try:
                addNewUser(data)
                return redirect("/login")
            except:
                print(sys.exc_info()[0])
                return redirect("/sign-up")
    else:
        return redirect("/")        


def addNewUser(data):
    sql = "INSERT INTO user (name, email, password) VALUES (?, ?, ?)";
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['name'])
    ibm_db.bind_param(stmt, 2, data['email'])
    ibm_db.bind_param(stmt, 3, data['password'])
    ibm_db.execute(stmt)

def signInUser(data):
    response = -1
    sql = "SELECT id FROM user WHERE email = ? AND password = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['email'])
    ibm_db.bind_param(stmt, 2, data['password'])
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    if tuple != False:
        response = tuple[0]
        session['userId'] = response
    return response    